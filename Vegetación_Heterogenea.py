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
# -----------------------------------
# 0 = zona húmeda
# 1 = zona seca

terreno = np.zeros_like(X)

zona_seca_1 = (X - 3.5)**2 + (Y - 2.5)**2 < 5
zona_seca_2 = (X + 4.0)**2 + (Y + 3.0)**2 < 4
zona_seca_3 = (X - 1.0)**2 + (Y + 5.0)**2 < 4.5
zona_seca_4 = (X + 2.5)**2 + (Y - 4.0)**2 < 3.5
zona_seca_5 = (X - 6.0)**2 + (Y + 1.0)**2 < 3.8

terreno[zona_seca_1] = 1
terreno[zona_seca_2] = 1
terreno[zona_seca_3] = 1
terreno[zona_seca_4] = 1
terreno[zona_seca_5] = 1

# -----------------------------------
# Velocidad de propagación
# -----------------------------------
R_humedo = 0.45
R_seco = 0.55

R = R_humedo + (R_seco - R_humedo) * terreno

# -----------------------------------
# Parámetros temporales
# -----------------------------------
dt = 0.02
num_steps = 600

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

    phi_y, phi_x = np.gradient(phi, dy, dx)
    grad_phi = np.sqrt(phi_x**2 + phi_y**2)

    # Actualización Hamilton-Jacobi
    phi = phi - dt * R * grad_phi

    quemado = phi < 0
    labels, num = label(quemado)

    etiqueta_foco = labels[N//2, N//2]

    if etiqueta_foco != 0:
        quemado_conectado = labels == etiqueta_foco
        desconectado = quemado & (~quemado_conectado)

        # Corrige zonas quemadas aisladas
        phi[desconectado] = np.abs(phi[desconectado])

    if n % 3 == 0:
        frames.append(phi.copy())

# -----------------------------------
# Visualización
# -----------------------------------
fig, ax = plt.subplots(figsize=(7, 7))

cmap_terreno = ListedColormap(["darkgreen", "lightgreen"])

def actualizar(k):

    ax.clear()
    phi_k = frames[k]

    # Terreno: húmedo/seco
    ax.imshow(
        terreno,
        extent=[-L, L, -L, L],
        origin="lower",
        cmap=cmap_terreno
    )

    # Zona quemada
    quemado = phi_k < 0
    ax.contourf(
        X, Y,
        quemado.astype(int),
        levels=[0.5, 1.5],
        colors=["black"]
    )

    # Frente
    ax.contour(
        X, Y,
        phi_k,
        levels=[0],
        colors="red",
        linewidths=2
    )
            # --- LEYENDA ---
    ax.plot([], [], color="darkgreen", linewidth=8, label="Vegetación húmeda")
    ax.plot([], [], color="lightgreen", linewidth=8, label="Vegetación seca")
    ax.plot([], [], color="black", linewidth=8, label="Zona quemada")
    ax.plot([], [], color="red", linewidth=2, label="Frente de incendio")

    ax.legend(loc="upper right")

    ax.set_title(f"Propagación en medio heterogéneo - t = {k*3*dt:.2f}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xlim(-L, L)
    ax.set_ylim(-L, L)
    ax.set_aspect("equal")

anim = FuncAnimation(fig, actualizar, frames=len(frames), interval=70)

anim.save("hetero.gif", writer=PillowWriter(fps=12))

plt.show()
