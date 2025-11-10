# 🪐 Simulador Orbital de Cuerpos Celestes   

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![GUI](https://img.shields.io/badge/Interface-CustomTkinter-green)
![Plotting](https://img.shields.io/badge/Visualization-Matplotlib-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Stable-success)

 <h3> Aplicación desarrollada en Python, que permite visualizar, analizar y comparar trayectorias orbitales de cometas, asteroides u otros objetos astronómicos mediante sus elementos keplerianos reales.<h3>
 <h3> El software utiliza ecuaciones de mecánica celeste de dos cuerpos (Sol–objeto) y presenta visualizaciones interactivas en 2D y 3D a través de una interfaz basada en CustomTkinter. <h3>

![Descargar Simulador Orbital](https://img.shields.io/badge/⬇️_Link_De_Descarga_del_Simulador-.exe-blue?style=for-the-badge)

https://github.com/PatricioHenrry/Simulador-Orbital-de-Cuerpos-Celestes/releases/download/untagged-531c169be3d340c184a7/Simulador_Orbital.exe


---

## ⚙️ Características Principales

-  **Simulación Kepleriana** de órbitas elípticas e hiperbólicas.  
-  **Comparación científica**: Halley (1P) vs ʻOumuamua (1I).  
-  **Visualizaciones 2D y 3D heliocéntricas** (proyección eclíptica).  
-  **Interfaz con CustomTkinter.**  
-  **Generación de ejecutable portable (.exe)** con PyInstaller.  
-  **Exportación de trayectorias** a CSV para análisis externo.  

---
## 🛠️ Tecnologías Utilizadas

-  Python 3.8+

-  CustomTkinter - Interfaz gráfica 

-  NumPy - Cálculos matemáticos y manipulación de arrays

-  Matplotlib - Visualización 2D y 3D

-  PyInstaller - Empaquetado a ejecutable
---
## 📏 Sistema de Unidades y Medidas

## Unidades Astronómicas (AU)
El simulador utiliza el sistema de Unidades Astronómicas para mantener coherencia y precisión en los cálculos orbitales:

- 1 AU = 149,597,870.7 km - Distancia promedio Tierra-Sol

- mu_sun = 0.01720209895² AU³/day² - Constante gravitacional heliocéntrica

- Todas las distancias se expresan en AU respecto al Sol (centro del sistema)

- La órbita terrestre se representa como un círculo de 1 AU de radio
---
## 🧮 Fundamento Científico

  El simulador implementa la **ecuación general del movimiento kepleriano**:

\[
r = \frac{a(1 - e^2)}{1 + e \cos(\nu)}
\]

  donde:  
- \(r\): distancia Sol–objeto (en UA)  
- \(a\): semi-eje mayor  
- \(e\): excentricidad  
- \(\nu\): anomalía verdadera  

  Las coordenadas perifocales \((x', y')\) se transforman al sistema eclíptico mediante:

\[
R = R_3(\Omega) R_1(i) R_3(\omega)
\]

  permitiendo obtener las posiciones tridimensionales en el espacio heliocéntrico.


---

## 🧱 Estructura del Proyecto
<h3>
  
```
Simulador Orbital de Cuerpos Celestes/
│
├── simulador_orbital_de_cuerpos_celestes.py
├── png.ico
├── requirements.txt
├── README.md
├── assets/
│   ├── halley_2d.png
│   ├── oumuamua_3d.png
│   └── comparacion_3d.png
└── .gitignore
```

---
## 🏗️ Estructura y Lógica del Código
```
# FLUJO PRINCIPAL DEL PROGRAMA
1. Configuración inicial de la interfaz (CustomTkinter)
2. Definición de constantes y funciones matemáticas
3. Base de datos de objetos celestes con parámetros orbitales
4. Funciones de conversión orbital → coordenadas cartesianas
5. Funciones de visualización (2D y 3D)
6. Interfaz de usuario con botones y controles
7. Loop principal de la aplicación
```
## 🧩 Módulos Principales
1. Conversión Orbital **(oe_to_state)**
   ```
   def oe_to_state(a, e, i_deg, raan_deg, argp_deg, nu_rad, mu=mu_sun):
    # Convierte elementos orbitales a coordenadas cartesianas 3D
    # Parámetros de entrada en grados, salida en AU
   ```
2. Propagación Orbital **(propagate_orbit)**
    ```
    def propagate_orbit(a, e, i_deg, raan_deg, argp_deg, nu_array):
    # Genera múltiples puntos de la órbita
    # Para visualización continua
     ```
3. Sistema de Coordenadas
 ```
    # Sistema de referencia heliocéntrico:
    # - Origen (0,0,0): Centro del Sol
    # - Plano XY: Plano eclíptica (órbita terrestre)
    # - Eje Z: Perpendicular al plano eclíptica
 ```
 4. Gestión de Objetos Celestes
 ```
    def get_object_params(nombre):
    objetos = {
        "Halley (1P)": (17.834, 0.96714, 162.26, 58.42, 111.33),
        # a (AU), e, i(°), Ω(°), ω(°)
    }
 ```
- # Transformación de Coordenadas
```
  # 1. Sistema perifocal → Sistema inercial
  R11 = cosO*cosw - sinO*sinw*cosi
  R12 = -cosO*sinw - sinO*cosw*cosi
  # ... matrices de rotación 3D
```
- # Manejo de Diferentes Tipos de Órbita
```
# Elíptica (e < 1): p = a(1-e²)
# Hiperbólica (e > 1): p = a(e²-1)
p = a * (1 - e**2) if e < 1.0 else abs(a) * (e**2 - 1)
```
---
## 🧩 Dependencias

```
customtkinter==5.2.2
matplotlib==3.9.2
numpy==2.1.1
pandas==2.2.3
```
## Instalación rápida:
```
pip install -r requirements.txt
```
---

## 👨‍💻 Autor
-  Patricio Henrry https://github.com/PatricioHenrry
  
Simulación Orbital Científica


