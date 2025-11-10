import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- VISUAL ---
ctk.set_appearance_mode("dark")  # "light", "dark", "system"
ctk.set_default_color_theme("blue")

# --- CONSTANTES ---
mu_sun = 0.01720209895**2  # Constante gravitacional heliocéntrica (AU^3/day^2)

def deg2rad(x): return x * np.pi / 180.0

def oe_to_state(a, e, i_deg, raan_deg, argp_deg, nu_rad, mu=mu_sun):
    i = deg2rad(i_deg)
    raan = deg2rad(raan_deg)
    argp = deg2rad(argp_deg)
    p = a * (1 - e**2) if e < 1.0 else abs(a) * (e**2 - 1)
    r = p / (1 + e * np.cos(nu_rad))
    x_per = r * np.cos(nu_rad)
    y_per = r * np.sin(nu_rad)

    cosO, sinO = np.cos(raan), np.sin(raan)
    cosi, sini = np.cos(i), np.sin(i)
    cosw, sinw = np.cos(argp), np.sin(argp)
    R11 = cosO*cosw - sinO*sinw*cosi
    R12 = -cosO*sinw - sinO*cosw*cosi
    R21 = sinO*cosw + cosO*sinw*cosi
    R22 = -sinO*sinw + cosO*cosw*cosi
    R31 = sinw*sini
    R32 = cosw*sini

    r_vec = np.array([
        R11*x_per + R12*y_per,
        R21*x_per + R22*y_per,
        R31*x_per + R32*y_per
    ])
    return r_vec

def propagate_orbit(a, e, i_deg, raan_deg, argp_deg, nu_array):
    Rs = [oe_to_state(a, e, i_deg, raan_deg, argp_deg, nu) for nu in nu_array]
    return np.array(Rs)

def get_object_params(nombre):
    objetos = {
        "Halley (1P)": (17.834, 0.96714, 162.26, 58.42, 111.33),
        "Oumuamua (1I)": (1.280, 1.20, 122.74, 24.60, 241.76),
        "Ejemplo elíptico": (3.0, 0.5, 10, 30, 45)
    }
    return objetos[nombre]

# --- VISUALIZACIÓN ---
def mostrar_graficos(tipo):
    nombre = combo.get()
    a, e, i_deg, raan_deg, argp_deg = get_object_params(nombre)
    nu_array = np.linspace(-np.pi, np.pi, 2000)
    Rs = propagate_orbit(a, e, i_deg, raan_deg, argp_deg, nu_array)
    theta_earth = np.linspace(0, 2*np.pi, 360)
    r_earth = np.column_stack([np.cos(theta_earth), np.sin(theta_earth), np.zeros_like(theta_earth)])

    if tipo == "2D":
        fig = plt.figure(figsize=(8,8))
        fig.canvas.manager.set_window_title(f"Proyección 2D - {nombre}")
        plt.plot(Rs[:,0], Rs[:,1], '-', label=f'{nombre}')
        plt.plot(r_earth[:,0], r_earth[:,1], '--', label='Órbita Tierra (1 AU)')
        plt.scatter([0],[0], color='orange', s=80, label='Sol')
        plt.axis('equal')
        plt.xlabel(r'$\mathbf{x\ (AU)}$', fontsize=12, fontweight='bold')
        plt.ylabel(r'$\mathbf{y\ (AU)}$', fontsize=12, fontweight='bold')
        plt.title(f'Trayectoria heliocéntrica (2D) - {nombre}', fontsize=13, fontweight='bold')
        plt.legend(); plt.grid(True); plt.show(block=False)

    elif tipo == "3D":
        fig = plt.figure(figsize=(9,6))
        fig.canvas.manager.set_window_title(f"Vista 3D - {nombre}")
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(Rs[:,0], Rs[:,1], Rs[:,2], '-', label=f'{nombre}')
        ax.plot(r_earth[:,0], r_earth[:,1], r_earth[:,2], '--', label='Tierra (1 AU)')
        ax.scatter([0],[0],[0], color='orange', s=60)
        ax.set_xlabel(r'$\mathbf{x\ (AU)}$', fontsize=11, fontweight='bold')
        ax.set_ylabel(r'$\mathbf{y\ (AU)}$', fontsize=11, fontweight='bold')
        ax.set_zlabel(r'$\mathbf{z\ (AU)}$', fontsize=11, fontweight='bold')
        ax.set_title(f'Órbita real de {nombre} (3D)', fontsize=13, fontweight='bold')
        ax.legend(); plt.show(block=False)

def mostrar_comparacion():
    halley = (17.834, 0.96714, 162.26, 58.42, 111.33)
    oumuamua = (1.280, 1.20, 122.74, 24.60, 241.76)

    nu_elip = np.linspace(-np.pi, np.pi, 2000)
    nu_obs = np.linspace(-np.deg2rad(60), np.deg2rad(60), 2000)
    lim = np.arccos(-1/1.20)
    nu_full = np.linspace(-lim, lim, 2000)

    R_halley = propagate_orbit(*halley, nu_elip)
    R_oumu_obs = propagate_orbit(*oumuamua, nu_obs)
    R_oumu_full = propagate_orbit(*oumuamua, nu_full)

    theta_earth = np.linspace(0, 2*np.pi, 360)
    r_earth = np.column_stack([np.cos(theta_earth), np.sin(theta_earth), np.zeros_like(theta_earth)])

    # 2D observable
    fig2d_obs = plt.figure(figsize=(8,8))
    fig2d_obs.canvas.manager.set_window_title("Comparación 2D (Tramo observable)")
    plt.plot(R_halley[:,0], R_halley[:,1], 'b-', label='Halley (Elíptica)')
    plt.plot(R_oumu_obs[:,0], R_oumu_obs[:,1], 'r-', label="'Oumuamua (Visible)")
    plt.plot(r_earth[:,0], r_earth[:,1], '--', color='gray', label='Tierra (1 AU)')
    plt.scatter([0],[0], color='orange', s=80, label='Sol')
    plt.axis('equal')
    plt.xlabel(r'$\mathbf{x\ (AU)}$', fontsize=12, fontweight='bold')
    plt.ylabel(r'$\mathbf{y\ (AU)}$', fontsize=12, fontweight='bold')
    plt.title("Comparación 2D - Tramo observable de 'Oumuamua", fontsize=13, fontweight='bold')
    plt.legend(); plt.grid(True)

    # 2D completa
    fig2d_full = plt.figure(figsize=(8,8))
    fig2d_full.canvas.manager.set_window_title("Comparación 2D (Órbita completa)")
    plt.plot(R_halley[:,0], R_halley[:,1], 'b-', label='Halley (Elíptica)')
    plt.plot(R_oumu_full[:,0], R_oumu_full[:,1], 'r-', label="'Oumuamua (Completa)")
    plt.plot(r_earth[:,0], r_earth[:,1], '--', color='gray', label='Tierra (1 AU)')
    plt.scatter([0],[0], color='orange', s=80, label='Sol')
    plt.axis('equal')
    plt.xlabel(r'$\mathbf{x\ (AU)}$', fontsize=12, fontweight='bold')
    plt.ylabel(r'$\mathbf{y\ (AU)}$', fontsize=12, fontweight='bold')
    plt.title("Comparación 2D - Órbita completa de 'Oumuamua", fontsize=13, fontweight='bold')
    plt.legend(); plt.grid(True)

    # 3D observable
    fig3d_obs = plt.figure(figsize=(9,6))
    fig3d_obs.canvas.manager.set_window_title("Comparación 3D (Tramo observable)")
    ax = fig3d_obs.add_subplot(111, projection='3d')
    ax.plot(R_halley[:,0], R_halley[:,1], R_halley[:,2], 'b-', label='Halley (Elíptica)')
    ax.plot(R_oumu_obs[:,0], R_oumu_obs[:,1], R_oumu_obs[:,2], 'r-', label="'Oumuamua (Visible)")
    ax.plot(r_earth[:,0], r_earth[:,1], r_earth[:,2], '--', color='gray', label='Tierra (1 AU)')
    ax.scatter([0],[0],[0], color='orange', s=60)
    ax.set_xlabel(r'$\mathbf{x\ (AU)}$', fontsize=11, fontweight='bold')
    ax.set_ylabel(r'$\mathbf{y\ (AU)}$', fontsize=11, fontweight='bold')
    ax.set_zlabel(r'$\mathbf{z\ (AU)}$', fontsize=11, fontweight='bold')
    ax.set_title("Comparación 3D - Tramo observable", fontsize=13, fontweight='bold')
    ax.legend()

    # 3D completa
    fig3d_full = plt.figure(figsize=(9,6))
    fig3d_full.canvas.manager.set_window_title("Comparación 3D (Órbita completa)")
    ax = fig3d_full.add_subplot(111, projection='3d')
    ax.plot(R_halley[:,0], R_halley[:,1], R_halley[:,2], 'b-', label='Halley (Elíptica)')
    ax.plot(R_oumu_full[:,0], R_oumu_full[:,1], R_oumu_full[:,2], 'r-', label="'Oumuamua (Completa)")
    ax.plot(r_earth[:,0], r_earth[:,1], r_earth[:,2], '--', color='gray', label='Tierra (1 AU)')
    ax.scatter([0],[0],[0], color='orange', s=60)
    ax.set_xlabel(r'$\mathbf{x\ (AU)}$', fontsize=11, fontweight='bold')
    ax.set_ylabel(r'$\mathbf{y\ (AU)}$', fontsize=11, fontweight='bold')
    ax.set_zlabel(r'$\mathbf{z\ (AU)}$', fontsize=11, fontweight='bold')
    ax.set_title("Comparación 3D - Órbita completa", fontsize=13, fontweight='bold')
    ax.legend(); plt.show(block=False)

# --- INTERFAZ ---
app = ctk.CTk()
app.title("🪐 Simulador Orbital de Cuerpos Celestes")
app.geometry("500x460")

title = ctk.CTkLabel(app, text=" 🪐 Simulador Orbital de Cuerpos Celestes 🪐 ",
                     font=("Roboto", 22, "bold"))
title.pack(pady=20)

label = ctk.CTkLabel(app, text="Seleccione el objeto astronómico:",
                     font=("Roboto", 15))
label.pack(pady=5)

combo = ctk.CTkOptionMenu(app,
                          values=["Halley (1P)", "Oumuamua (1I)", "Ejemplo elíptico"])
combo.set("Halley (1P)")
combo.pack(pady=10)

btn1 = ctk.CTkButton(app, text="🌍 Proyección 2D",
                     command=lambda: mostrar_graficos("2D"), width=250, height=40)
btn1.pack(pady=10)

btn2 = ctk.CTkButton(app, text="🪐 Órbita 3D",
                     command=lambda: mostrar_graficos("3D"), width=250, height=40)
btn2.pack(pady=10)

btn3 = ctk.CTkButton(app, text="🌌 Comparar Halley vs Oumuamua",
                     command=mostrar_comparacion, width=250, height=40)
btn3.pack(pady=15)

footer = ctk.CTkLabel(app, text="© Simulación Orbital Científica - Patricio Henrry",
                      font=("Roboto", 12))
footer.pack(side="bottom", pady=10)

app.mainloop()
