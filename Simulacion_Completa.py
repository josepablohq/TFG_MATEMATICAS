#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import ListedColormap
from scipy.ndimage import label


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
# Terreno heterogéneo
# 0 = húmedo
# 1 = seco
# -----------------------------------
terreno = np.zeros_like(X)

zonas_secas = [
    (X - 3.5)**2 + (Y - 2.5)**2 < 5,
    (X + 4.0)**2 + (Y + 3.0)**2 < 4,
    (X - 1.0)**2 + (Y + 5.0)**2 < 4.5,
    (X + 2.5)**2 + (Y - 4.0)**2 < 3.5,
    (X - 6.0)**2 + (Y + 1.0)**2 < 3.8
]

for zona in zonas_secas:
    terreno[zona] = 1


# -----------------------------------
# Velocidad base del terreno
# -----------------------------------

R_humedo = 0.45
R_seco = 0.55

R_terreno = R_humedo + (R_seco - R_humedo) * terreno


# -----------------------------------
# Parámetros físicos
# -----------------------------------
intensidad_viento = 0.7
intensidad_pendiente = 0.4


# -----------------------------------
# Parámetros temporales
# -----------------------------------
dt = 0.015
num_steps = 800


# -----------------------------------
# Condición inicial
# -----------------------------------
radio_inicial = 1.0

phi = np.sqrt(X**2 + Y**2) - radio_inicial


# -----------------------------------
# Evolución temporal
# -----------------------------------
frames = []

for n in range(num_steps):

    # Gradiente espacial
    phi_y, phi_x = np.gradient(phi, dy, dx)
    grad_phi = np.sqrt(phi_x**2 + phi_y**2) + 1e-8

    # Dirección normal del frente
    nx = phi_x / grad_phi
    ny = phi_y / grad_phi

    # Viento hacia la izquierda (-x)
    factor_viento = 1 + intensidad_viento * np.maximum(-nx, 0)

    # Pendiente hacia abajo (-y)
    factor_pendiente = 1 + intensidad_pendiente * np.maximum(ny, 0)

    # Velocidad total
    R = R_terreno * factor_viento * factor_pendiente

    # Actualización Hamilton-Jacobi
    phi = phi - dt * R * grad_phi

    # Evitar focos desconectados
    quemado_total = phi < 0

    labels, num = label(quemado_total)

    etiqueta_foco = labels[N // 2, N // 2]

    if etiqueta_foco != 0:
        quemado_conectado = labels == etiqueta_foco
        desconectado = quemado_total & (~quemado_conectado)

        phi[desconectado] = np.abs(phi[desconectado])

    # Guardar frames cada 3 pasos
    if n % 3 == 0:
        frames.append(phi.copy())


# -----------------------------------
# Visualización
# -----------------------------------
fig, ax = plt.subplots(figsize=(8, 7))

cmap_terreno = ListedColormap(["darkgreen","lightgreen"])

def actualizar(k):

    ax.clear()

    phi_k = frames[k]

    # Terreno
    ax.imshow(terreno, extent=[-L, L, -L, L], origin="lower", cmap=cmap_terreno)

    # -----------------------------------
    # Franja lateral de altitud
    # -----------------------------------
    
    gradiente_altitud = np.linspace(1, 0, 200).reshape(-1, 1)

    ax.imshow(gradiente_altitud, extent=[10.6, 11.2, -L, L], cmap="terrain", aspect="auto", origin="lower")

    ax.text(11.35, 8, "Mayor\naltitud", fontsize=6, va="center")

    ax.text(11.35, -8,"Menor\naltitud",fontsize=6, va="center")

    ax.text(11.9, 0, "Pendiente", rotation=90, fontsize=9, va="center")

    # Campo de viento hacia la izquierda
    x_flechas = np.linspace(-8, 8, 9)
    y_flechas = np.linspace(-8, 8, 9)

    Xf, Yf = np.meshgrid(x_flechas, y_flechas)

    U = -np.ones_like(Xf)
    V = np.zeros_like(Yf)

    ax.quiver(
        Xf, Yf,
        U, V,
        color="white",
        angles="xy",
        scale_units="xy",
        scale=1.5,
        width=0.004,
        alpha=0.8)

    # Zona quemada
    quemado = phi_k < 0

    ax.contourf(X, Y, quemado.astype(int), levels=[0.5, 1.5], colors=["black"])

    # Frente de incendio
    ax.contour(X, Y, phi_k, levels=[0], colors="red", linewidths=2)

    # Leyenda
    ax.plot([], [], color="darkgreen", linewidth=8,label="Vegetación húmeda")
    ax.plot([], [], color="lightgreen", linewidth=8,label="Vegetación seca")
    ax.plot([], [], color="black", linewidth=8,label="Zona quemada")
    ax.plot([], [], color="red", linewidth=2,label="Frente de incendio")
    ax.plot([], [], color="whitesmoke", marker="<", markersize=10, linewidth=2, label="Dirección del viento")
    ax.legend(loc="lower left",fontsize=8)

    # Ajustes gráficos
    ax.set_title(f"Simulación completa - t = {k * 3 * dt:.2f}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xlim(-L, 12.4)
    ax.set_ylim(-L, L)
    ax.set_aspect("equal")


# -----------------------------------
# Crear animación
# -----------------------------------
anim = FuncAnimation(fig, actualizar, frames=len(frames), interval=70)


# -----------------------------------
# Guardar GIF
# -----------------------------------
anim.save("Completo.gif", writer=PillowWriter(fps=12))

plt.show()


# In[ ]:




