# Evolución geométrica del frente de incendio mediante ecuaciones en derivadas parciales

## Descripción

Este repositorio contiene los programas desarrollados para el Trabajo Fin de Grado *Evolución geométrica del frente de incendio: modelización y simulación numérica*, realizado en el Grado en Matemáticas de la Universidad de Almería.

El objetivo del proyecto es estudiar la propagación de incendios forestales mediante técnicas de modelización matemática basadas en ecuaciones en derivadas parciales. En particular, se emplea una formulación de Hamilton–Jacobi para describir la evolución geométrica del frente de incendio y se desarrollan distintas simulaciones numéricas en Python para analizar la influencia de diversos factores sobre su propagación.

---

## Fundamento matemático

El modelo considera el frente de incendio como una interfaz móvil cuya evolución viene descrita por la ecuación

[
\frac{\partial \phi}{\partial t} + R(x,y),|\nabla \phi| = 0,
]

donde:

* (\phi(x,y,t)) es la función de nivel asociada al frente de incendio.
* (R(x,y)) representa la velocidad local de propagación.
* El conjunto (\phi=0) describe la posición del frente en cada instante.

La velocidad de propagación se inspira en el modelo de Rothermel e incorpora distintos factores relacionados con el combustible, el viento y la pendiente del terreno.

---

## Contenido del repositorio

### 1. Incendio homogéneo

Simulación básica con velocidad de propagación constante en todo el dominio.

Características:

* Terreno homogéneo.
* Sin viento.
* Sin pendiente.
* Propagación circular del frente.

---

### 2. Vegetación heterogénea

Se consideran distintas regiones del terreno con velocidades de propagación diferentes.

Características:

* Vegetación seca.
* Vegetación húmeda.
* Velocidad dependiente de la posición.

---

### 3. Vegetación heterogénea y viento

Extensión del caso anterior incorporando la influencia del viento.

Características:

* Terreno heterogéneo.
* Viento dominante.
* Propagación asimétrica del frente.

---

### 4. Simulación completa

Modelo que combina todos los factores considerados en el trabajo.

Características:

* Terreno heterogéneo.
* Influencia del viento.
* Influencia de la pendiente.
* Evolución geométrica compleja del frente.

---

### 5. Validación inspirada en el incendio de Losacio (Zamora, 2022)

Simulación desarrollada para comparar el comportamiento del modelo con un caso real.

Características:

* Cuatro tipos de superficie.
* Distribución espacial inspirada en datos reales.
* Comparación de la superficie afectada.
* Estimación del error relativo respecto al incendio real.

---

## Bibliotecas utilizadas

Los programas han sido desarrollados en Python utilizando principalmente:

* NumPy
* Matplotlib
* SciPy

---

## Resultados

Las simulaciones permiten analizar cómo factores como:

* el tipo de combustible,
* la dirección del viento,
* la pendiente del terreno,

modifican la velocidad de propagación y la geometría del frente de incendio.

Asimismo, la comparación con el incendio de Losacio muestra que, pese a las simplificaciones adoptadas, el modelo reproduce de forma razonable algunos comportamientos generales observados en incendios forestales reales.

---

## Autor

José Pablo Hernández Quintana

Grado en Matemáticas

Universidad de Almería

Curso 2025–2026
