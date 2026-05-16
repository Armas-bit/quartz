import os
import json
import re
import subprocess
import requests
from pathlib import Path
from urllib.parse import quote

# ============================
# CONFIGURACIÓN — EDITA AQUÍ
# ============================
CLICKUP_TOKEN = "pk_162137814_VSWSYU11V3AXPNMMDMJ8RZYYCQZZE1R4"
WORKSPACE_ID = "90132299356"
OBSIDIAN_VAULT = r"C:\Users\FABRICIO\Documents\Obsidian Memory"
QUARTZ_DIR = r"C:\Windows\System32\quartz"
GITHUB_USER = "Armas-bit"
PROCESADOS_FILE = r"C:\Windows\System32\quartz\procesados.json"

# Mapa de (CURSO, UNIDAD) → ID del doc CLASES en ClickUp
DOC_MAP = {
    ("ECONOMÍA I", "UNIDAD I"):              "2ky4vfjw-2113",
    ("ECONOMÍA I", "UNIDAD II"):             "2ky4vfjw-3033",
    ("DERECHO CONSTITUCIONAL", "UNIDAD I"):  "2ky4vfjw-2233",
    ("NEGOCIOS GLOBALES", "UNIDAD I"):       "2ky4vfjw-2853",
    ("NEGOCIOS GLOBALES", "UNIDAD II"):      "2ky4vfjw-4073",
    ("TRC", "UNIDAD I"):                     "2ky4vfjw-2673",
    ("TRC", "UNIDAD II"):                    "2ky4vfjw-4093",
    ("MATEMÁTICA I", "UNIDAD I"):            "2ky4vfjw-2933",
    ("MATEMÁTICA I", "UNIDAD II"):           "2ky4vfjw-4053",
    ("MDI", "UNIDAD I"):                     "2ky4vfjw-2273",
}

# ============================
# FUNCIONES
# ============================

def cargar_procesados():
    if os.path.exists(PROCESADOS_FILE):
        with open(PROCESADOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_procesados(data):
    with open(PROCESADOS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def leer_tags(filepath):
    """Lee las etiquetas del frontmatter de una nota de Obsidian."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return []

    frontmatter = match.group(1)
    tags_match = re.search(r"tags:\s*\[(.+?)\]", frontmatter)
    if not tags_match:
        return []

    tags = [t.strip().strip('"').strip("'").upper() for t in tags_match.group(1).split(",")]
    return tags

def extraer_info(tags):
    """Extrae curso, unidad y semana de las etiquetas."""
    curso = None
    unidad = None
    semana = None

    cursos_conocidos = [k[0] for k in DOC_MAP.keys()]

    for tag in tags:
        if tag.startswith("SEMANA"):
            semana = tag
        elif tag.startswith("UNIDAD"):
            unidad = tag
        elif tag.startswith("CICLO"):
            pass  # ignorar
        elif tag in cursos_conocidos:
            curso = tag

    return curso, unidad, semana

def construir_url_quartz(filepath):
    """Construye la URL de Quartz para una nota dada su ruta."""
    rel = os.path.relpath(filepath, OBSIDIAN_VAULT)
    rel_sin_ext = os.path.splitext(rel)[0]
    partes = rel_sin_ext.replace("\\", "/").split("/")
    partes_encoded = [quote(p) for p in partes]
    return f"https://{GITHUB_USER}.github.io/quartz/{'/'.join(partes_encoded)}"

def pagina_ya_existe(doc_id, semana):
    """Verifica si ya existe una página con ese nombre en el doc."""
    url = f"https://api.clickup.com/api/v3/workspaces/{WORKSPACE_ID}/docs/{doc_id}/pages"
    headers = {"Authorization": CLICKUP_TOKEN}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return False
    data = response.json()
    pages = data if isinstance(data, list) else data.get("pages", [])
    for page in pages:
        if page.get("name", "").upper() == semana.upper():
            return True
    return False

def crear_pagina_clickup(doc_id, semana, quartz_url, nombre_nota):
    """Crea una nueva página en el doc CLASES de ClickUp."""
    url = f"https://api.clickup.com/api/v3/workspaces/{WORKSPACE_ID}/docs/{doc_id}/pages"
    headers = {
        "Authorization": CLICKUP_TOKEN,
        "Content-Type": "application/json"
    }
    body = {
        "name": semana,
        "content": f"# {nombre_nota}\n\n[Ver nota en Quartz]({quartz_url})"
    }
    response = requests.post(url, headers=headers, json=body)
    return response.status_code in [200, 201]

def sincronizar_quartz():
    """Copia notas a Quartz y hace push a GitHub."""
    print("\n📁 Copiando notas a Quartz...")
    subprocess.run([
        "robocopy",
        OBSIDIAN_VAULT,
        os.path.join(QUARTZ_DIR, "content"),
        "/MIR", "/XD", ".obsidian"
    ])

    print("📤 Subiendo a GitHub...")
    os.chdir(QUARTZ_DIR)
    subprocess.run(["git", "add", "."])
    result = subprocess.run(["git", "commit", "-m", "actualizar notas"], capture_output=True, text=True)
    if "nothing to commit" in result.stdout:
        print("✅ No hay cambios nuevos en las notas.")
    else:
        subprocess.run(["git", "push"])
        print("✅ Notas publicadas en Quartz.")

# ============================
# PROGRAMA PRINCIPAL
# ============================

def main():
    procesados = cargar_procesados()
    nuevas = 0

    print("🔍 Revisando notas de Obsidian...\n")

    for filepath in Path(OBSIDIAN_VAULT).rglob("*.md"):
        # Ignorar archivos de configuración de Obsidian
        if ".obsidian" in str(filepath):
            continue

        key = str(filepath)
        mtime = os.path.getmtime(filepath)

        # Solo procesar notas nuevas o modificadas
        if key in procesados and procesados[key] == mtime:
            continue

        tags = leer_tags(filepath)
        if not tags:
            continue

        curso, unidad, semana = extraer_info(tags)

        if not curso or not unidad or not semana:
            continue

        doc_id = DOC_MAP.get((curso, unidad))
        if not doc_id:
            print(f"⚠️  No encontré doc CLASES para {curso} / {unidad}")
            continue

        quartz_url = construir_url_quartz(filepath)
        nombre_nota = filepath.stem

        if pagina_ya_existe(doc_id, semana):
            print(f"✅ Ya existe página '{semana}' en {curso} / {unidad}, omitiendo.")
        else:
            ok = crear_pagina_clickup(doc_id, semana, quartz_url, nombre_nota)
            if ok:
                print(f"✅ Página creada: {curso} / {unidad} / {semana}")
                nuevas += 1
            else:
                print(f"❌ Error al crear página para {nombre_nota}")

        procesados[key] = mtime

    guardar_procesados(procesados)

    if nuevas == 0:
        print("ℹ️  No hay páginas nuevas para crear en ClickUp.")

    sincronizar_quartz()
    print("\n🎉 ¡Todo listo!")
    input("\nPresiona Enter para cerrar...")

if __name__ == "__main__":
    main()
