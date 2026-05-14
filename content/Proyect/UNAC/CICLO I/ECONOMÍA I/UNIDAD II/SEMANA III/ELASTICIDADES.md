---
tags:
  - CICLO I
  - UNIDAD II
  - SEMANA III
  - ECONOMÍA
autosync-database:
  - UNAC
NotionID-UNAC: 35e75f76-e3d2-814c-bf2e-c447f53c8cd8
link-UNAC: https://www.notion.so/ELASTICIDADES-35e75f76e3d2814cbf2ec447f53c8cd8
---

# TIPOS DE ELASTICIDAD PRECIO DEMANDA

| TIPO                     | VALOR        | RESPUESTA    |
| ------------------------ | ------------ | ------------ |
| Perfectamente Inelastica | \|E\| = 0    | Nula         |
| Inelástica               | 0<\|E\|<1    | Débil        |
| Unitaria                 | \|E\| =1     | Proporcional |
| Elástica                 | \|E\|>1      | Fuerte       |
| Perfectamente elástica   | \|E\| --> ♾️ | Infinita     |
## FÓRMULA ELASTICIDAD PRECIO DEMANDA
$$E_p^D = \frac{\% \Delta Q_D}{\% \Delta P} = \frac{\Delta Q_D}{\Delta P} \cdot \frac{P}{Q_D}$$
	Esta siempre va a ser negativa por su naturaleza. Se trabaja con el valor absoluto

# FÓRMULA ELASTICIDAD PRECIO OFERTA
$$E_p^O = \frac{\% \Delta Q_O}{\% \Delta P} = \frac{\Delta Q_O}{\Delta P} \cdot \frac{P}{Q_O}$$

| VALOR | TIPO       |
| ----- | ---------- |
| E<1   | Inelástica |
| E=0   | Unitaria   |
| E>1   | Elástica   |


```chartsview
#-----------------------------------------
# Chart Options
#-----------------------------------------
type: Line
options:
  xField: "precio"
  yField: "cantidad"
  seriesField: "tipo"
  smooth: false
  xAxis:
    title:
      text: "Precio P"
  yAxis:
    title:
      text: "Cantidad Q"

#-----------------------------------------
# Chart Data
#-----------------------------------------
data:
  - precio: 0
    cantidad: 0
    tipo: "Elástica"
  - precio: 1
    cantidad: 2
    tipo: "Elástica"
  - precio: 2
    cantidad: 4
    tipo: "Elástica"
  - precio: 3
    cantidad: 6
    tipo: "Elástica"
  - precio: 4
    cantidad: 8
    tipo: "Elástica"
  - precio: 5
    cantidad: 10
    tipo: "Elástica"
  - precio: 0
    cantidad: 0
    tipo: "Inelástica"
  - precio: 1
    cantidad: 0.5
    tipo: "Inelástica"
  - precio: 2
    cantidad: 1
    tipo: "Inelástica"
  - precio: 3
    cantidad: 1.5
    tipo: "Inelástica"
  - precio: 4
    cantidad: 2
    tipo: "Inelástica"
  - precio: 5
    cantidad: 2.5
    tipo: "Inelástica"
```

# ELASTICIDAD INGRESO DEMANDA

$$E_Y = \frac{\% \Delta Q_D}{\% \Delta Y}$$

| TIPO DE BIEN          | VALOR  |
| --------------------- | ------ |
| Normal Superior(lujo) | E>1    |
| Normal Necesario      | 0<E<=1 |
| Inferior              | E<0    |

# ELASTICIDAD CRUZADA

$$E_{XY} = \frac{\% \Delta Q_{D_X}}{\% \Delta P_Y}$$
> ES PARA SABER LA RELACION ENTRE 2 BIENES
> 	Exy > 0 --> SUSTITUTOS
> 	Exy < 0 --> COMPLEMENTARIOS
> 	Exy = 0 --> INDEPENDIENTES