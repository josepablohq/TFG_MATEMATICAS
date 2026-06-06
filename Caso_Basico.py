#!/usr/bin/env python
# coding: utf-8

# In[9]:


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# -----------------------------------
# Dominio espacial
# -----------------------------------
N = 250
L = 10

x = np.linspace(-L, L, N)
y = np.linspace(-L, L, N)

X, Y = np.meshgrid(x, y)

dx = x[1] - x[0]
dy = y[1] - y[0]

# -----------------------------------
# Parámetros del modelo
# -----------------------------------
R = 0.8
dt = 0.03
num_steps = 250

# -----------------------------------
# Condición inicial
# Frente circular inicial
# -----------------------------------
radio_inicial = 0.1

phi = np.sqrt(X**2 + Y**2) - radio_inicial

# -----------------------------------
# Evolución temporal
# -----------------------------------
frames = []

for n in range(num_steps):

    # Gradiente espacial
    phi_y, phi_x = np.gradient(phi, dy, dx)

    grad_phi = np.sqrt(phi_x**2 + phi_y**2)

    # Actualización temporal
    phi = phi - dt * R * grad_phi

    if n % 3 == 0:
        frames.append(phi.copy())

# -----------------------------------
# Visualización
# -----------------------------------
fig, ax = plt.subplots(figsize=(7,7))

def actualizar(k):

    ax.clear()

    phi_k = frames[k]

    # Fondo verde (zona no quemada)
    ax.contourf(
        X, Y,
        phi_k,
        levels=[0, phi_k.max()],
        colors=["green"]
    )

    # Zona quemada (negro)
    ax.contourf(
        X, Y,
        phi_k,
        levels=[phi_k.min(), 0],
        colors=["black"]
    )

    # Frente de incendio (rojo)
    ax.contour(
        X, Y,
        phi_k,
        levels=[0],
        colors="red",
        linewidths=2
    )

        # --- LEYENDA ---
    ax.plot([], [], color="green", linewidth=8, label="Vegetación homogénea")
    ax.plot([], [], color="black", linewidth=8, label="Zona quemada")
    ax.plot([], [], color="red", linewidth=2, label="Frente de incendio")

    ax.legend(loc="upper right")

    ax.set_title(f"Propagación del incendio - t = {k*3*dt:.2f}")

    ax.set_xlim(-L, L)
    ax.set_ylim(-L, L)

    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ax.set_aspect("equal")

anim = FuncAnimation(
    fig,
    actualizar,
    frames=len(frames),
    interval=70
)

# Guardar GIF
anim.save(
    "Basico.gif",
    writer=PillowWriter(fps=12)
)

plt.show()


# In[ ]:




