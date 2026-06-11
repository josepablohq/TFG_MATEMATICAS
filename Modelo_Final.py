import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.colors import ListedColormap
from scipy.ndimage import label, gaussian_filter


# Dominio espacial en km

N = 250
L = 10
x = np.linspace(-L, L, N)
y = np.linspace(-L, L, N)
X, Y = np.meshgrid(x, y)

dx = x[1] - x[0]
dy = y[1] - y[0]

area_celda_ha = dx * dy * 100
area_real_ha = 31473.13


# Terreno heterogéneo inspirado en Losacio
# 0 = forestal arbolado
# 1 = forestal no arbolado
# 2 = no forestal
# 3 = improductivo

np.random.seed(4)

ruido = gaussian_filter(np.random.rand(N, N), sigma=10)
ruido = (ruido - ruido.min()) / (ruido.max() - ruido.min())

terreno = np.zeros_like(X, dtype=int)

q1 = np.quantile(ruido, 0.469)
q2 = np.quantile(ruido, 0.469 + 0.363)
q3 = np.quantile(ruido, 0.469 + 0.363 + 0.157)

terreno[ruido > q1] = 1
terreno[ruido > q2] = 2
terreno[ruido > q3] = 3


# Velocidades de propagación

R_arbolada = 0.42
R_noarbolada = 0.50
R_noforestal = 0.26
R_improductiva = 0.08

R_terreno = np.zeros_like(X)
R_terreno[terreno == 0] = R_arbolada
R_terreno[terreno == 1] = R_noarbolada
R_terreno[terreno == 2] = R_noforestal
R_terreno[terreno == 3] = R_improductiva


# Parámetros físicos y temporales

intensidad_viento = 0.7
intensidad_pendiente = 0.4

dt = 0.01
num_steps = 550


# Condición inicial

radio_inicial = 1.0
phi = np.sqrt(X**2 + Y**2) - radio_inicial


# Evolución temporal

frames = []
areas = []

for n in range(num_steps):

    phi_y, phi_x = np.gradient(phi, dy, dx)
    grad_phi = np.sqrt(phi_x**2 + phi_y**2) + 1e-8

    nx = phi_x / grad_phi
    ny = phi_y / grad_phi

    # Viento hacia la izquierda y pendiente hacia abajo
    
    factor_viento = 1 + intensidad_viento * np.maximum(-nx, 0)
    factor_pendiente = 1 + intensidad_pendiente * np.maximum(ny, 0)

    R = R_terreno * factor_viento * factor_pendiente

    phi = phi - dt * R * grad_phi

    # Eliminar focos desconectados
    
    quemado_total = phi < 0
    labels, num = label(quemado_total)

    etiqueta_foco = labels[N // 2, N // 2]

    if etiqueta_foco != 0:
        quemado_conectado = labels == etiqueta_foco
        desconectado = quemado_total & (~quemado_conectado)
        phi[desconectado] = np.abs(phi[desconectado])

    areas.append(np.sum(phi < 0) * area_celda_ha)

    if n % 3 == 0:
        frames.append(phi.copy())


# Resultados finales

area_simulada = np.sum(phi < 0) * area_celda_ha
error = abs(area_simulada - area_real_ha) / area_real_ha * 100

print("RESULTADOS FINALES")
print("------------------")
print(f"Superficie real: {area_real_ha:.2f} ha")
print(f"Superficie simulada: {area_simulada:.2f} ha")
print(f"Error relativo: {error:.2f} %")


# Visualización

fig, ax = plt.subplots(figsize=(8, 7))

cmap_terreno = ListedColormap([
    "darkgreen",   # forestal arbolado
    "lightgreen",  # forestal no arbolado
    "khaki",       # no forestal
    "gray"         # improductivo
])


def actualizar(k):

    ax.clear()
    phi_k = frames[k]

    # Terreno
    ax.imshow(
        terreno,
        extent=[-L, L, -L, L],
        origin="lower",
        cmap=cmap_terreno)

    # Franja lateral de altitud
    
    gradiente_altitud = np.linspace(1, 0, 200).reshape(-1, 1)

    ax.imshow(
        gradiente_altitud,
        extent=[10.6, 11.2, -L, L],
        cmap="terrain",
        aspect="auto",
        origin="lower")

    ax.text(11.35, 8, "Mayor\naltitud", fontsize=6, va="center")
    ax.text(11.35, -8, "Menor\naltitud", fontsize=6, va="center")
    ax.text(11.9, 0, "Pendiente", rotation=90, fontsize=9, va="center")

    # Viento hacia la izquierda
    
    Xf, Yf = np.meshgrid(np.linspace(-8, 8, 9), np.linspace(-8, 8, 9))

    ax.quiver(
        Xf, Yf,
        -np.ones_like(Xf), np.zeros_like(Yf),
        color="white",
        angles="xy",
        scale_units="xy",
        scale=1.5,
        width=0.004,
        alpha=0.8)

    # Zona quemada y frente
    
    quemado = phi_k < 0

    ax.contourf(X, Y, quemado.astype(int), levels=[0.5, 1.5], colors=["black"], alpha=0.85)

    ax.contour(X, Y, phi_k, levels=[0], colors="red", linewidths=2)

    # Leyenda

    ax.plot([], [], color="darkgreen", linewidth=8, label="Forestal arbolado")
    ax.plot([], [], color="lightgreen", linewidth=8, label="Forestal no arbolado")
    ax.plot([], [], color="khaki", linewidth=8, label="No forestal")
    ax.plot([], [], color="gray", linewidth=8, label="Improductivo")
    ax.plot([], [], color="black", linewidth=8, label="Zona quemada")
    ax.plot([], [], color="red", linewidth=2, label="Frente de incendio")
    ax.plot([], [], color="whitesmoke", marker="<", markersize=10,
            linewidth=2, label="Dirección del viento")

    ax.legend(loc="lower left", fontsize=8)

    ax.set_title(f"Simulación inspirada en Losacio - t = {k * 3 * dt:.2f}")
    ax.set_xlabel("x (km)")
    ax.set_ylabel("y (km)")
    ax.set_xlim(-L, 12.4)
    ax.set_ylim(-L, L)
    ax.set_aspect("equal")

# Animación

anim = FuncAnimation(fig, actualizar, frames=len(frames), interval=70)
anim.save("Losacio_aproximado.gif", writer=PillowWriter(fps=12))

plt.show()

# Gráfica de evolución de la superficie quemada

tiempos = np.arange(len(areas)) * dt

plt.figure(figsize=(7, 4))
plt.plot(tiempos, areas, linewidth=2)

plt.xlabel("Tiempo simulado")
plt.ylabel("Superficie quemada (ha)")
plt.title("Evolución de la superficie afectada durante la simulación")
plt.grid(True)

plt.savefig("Evolucion_temporal_superficie.png", dpi=300, bbox_inches="tight")
plt.show()
