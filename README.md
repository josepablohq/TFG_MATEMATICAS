# Evolución geométrica del frente de incendio mediante ecuaciones en derivadas parciales

## Descripción

Este repositorio contiene los programas desarrollados para el Trabajo Fin de Grado **"Evolución geométrica del frente de incendio: modelización y simulación numérica"**, realizado en el Grado en Matemáticas de la Universidad de Almería.

El objetivo del proyecto es estudiar la propagación de incendios forestales mediante técnicas de modelización matemática basadas en ecuaciones en derivadas parciales (EDP). Para ello, se emplea una formulación de Hamilton-Jacobi que permite describir la evolución geométrica del frente de incendio como una interfaz en movimiento.

A partir de esta formulación se desarrollan distintas simulaciones numéricas en Python que permiten analizar la influencia del combustible, el viento y la pendiente sobre la propagación del fuego.

---

## Fundamento matemático

El frente de incendio se representa mediante una función de nivel `phi(x,y,t)`, definida de forma que:

```text
phi(x,y,t) < 0   Zona quemada

phi(x,y,t) = 0   Frente de incendio

phi(x,y,t) > 0   Combustible no quemado
```

La evolución temporal del frente viene descrita mediante una ecuación de Hamilton-Jacobi:

```text
d(phi)/dt + R(x,y) · |grad(phi)| = 0
```

donde:

* `phi(x,y,t)` representa la función de nivel.
* `R(x,y)` representa la velocidad local de propagación.
* `|grad(phi)|` representa la norma del gradiente espacial.
* La curva `phi = 0` identifica la posición del frente de incendio.

La discretización utilizada en las simulaciones conduce a la actualización iterativa:

```text
phi_nueva = phi_actual - dt · R · |grad(phi)|
```

La velocidad de propagación se inspira en el modelo de Rothermel y se modifica mediante distintos factores asociados al terreno:

```text
R = R_terreno · factor_viento · factor_pendiente
```

---

## Estructura del repositorio

### Incendio homogéneo

Simulación básica utilizada para comprobar el comportamiento del modelo.

Características:

* Velocidad constante.
* Terreno homogéneo.
* Sin viento.
* Sin pendiente.

Resultado esperado:

* Propagación circular del frente de incendio.

---

### Vegetación heterogénea

Se consideran distintas regiones del terreno con velocidades de propagación diferentes.

Características:

* Vegetación seca.
* Vegetación húmeda.
* Velocidad dependiente de la posición.

Resultado esperado:

* Deformación del frente al atravesar regiones con distinta capacidad de propagación.

---

### Vegetación heterogénea y viento

Se incorpora el efecto de un viento dominante.

Características:

* Terreno heterogéneo.
* Influencia del viento.
* Propagación direccional.

Resultado esperado:

* Avance preferente del frente en la dirección del viento.

---

### Simulación completa

Modelo que combina todos los factores considerados en el trabajo.

Características:

* Terreno heterogéneo.
* Viento.
* Pendiente.
* Velocidad de propagación variable.

Resultado esperado:

* Evolución geométrica compleja del frente de incendio.

---

### Validación inspirada en el incendio de Losacio (Zamora, 2022)

Simulación desarrollada para comparar el comportamiento general del modelo con un incendio forestal real.

Características:

* Cuatro tipos de superficie:

  * Forestal arbolada.
  * Forestal no arbolada.
  * No forestal.
  * Improductiva.
* Distribución espacial heterogénea.
* Influencia del viento y la pendiente.
* Cálculo de la superficie afectada.

La comparación se realiza utilizando la superficie total quemada registrada en el incendio de Losacio y la obtenida mediante la simulación.

---

## Bibliotecas utilizadas

Los programas han sido desarrollados en Python utilizando las siguientes bibliotecas:

### NumPy

Utilizada para:

* Cálculo numérico.
* Operaciones matriciales.
* Generación de mallas espaciales.

### Matplotlib

Utilizada para:

* Representación gráfica de resultados.
* Visualización del frente de incendio.
* Generación de animaciones GIF.

### SciPy

Utilizada para:

* Procesamiento de regiones del terreno.
* Suavizado mediante filtros gaussianos.
* Identificación de zonas conectadas.

---

## Resultados

Las simulaciones permiten analizar de forma cualitativa la influencia de distintos factores sobre la evolución geométrica del frente de incendio.

Los resultados obtenidos muestran que:

* El viento favorece la propagación en una dirección preferente.
* La pendiente modifica la velocidad local de avance.
* La heterogeneidad del combustible produce deformaciones en el frente.
* La combinación de estos factores genera patrones de propagación más próximos a los observados en incendios reales.

Además, la validación realizada con el incendio de Losacio permite evaluar las capacidades y limitaciones del modelo empleado.

---

## Autor

José Pablo Hernández Quintana

Trabajo Fin de Grado en Matemáticas

Universidad de Almería

Curso académico 2025–2026

---

## Licencia

Este repositorio se distribuye con fines exclusivamente académicos y docentes.
