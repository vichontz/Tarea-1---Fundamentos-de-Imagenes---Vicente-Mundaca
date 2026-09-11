
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2
from skimage import img_as_float
from skimage.io import imsave, imread
from pathlib import Path
from ColorSaturation import color_saturation


# 1)    Construya y grafique al menos tres configuraciones distintas de puntos de control, incluyendo 
#       una que aumente selectivamente un intervalo de tonos, una que atenúe otro intervalo y una 
#       que combine aumentos y disminuciones en distintos tonos.

#hay q definir 3 conjuntos de puntos de control (hI,mi).

#para HSL:
#0°  : Rojo
#60° : Amarillo
#120°: Verde
#180°: Cian
#240°: Azul 
#300°: Magenta

P_aumento =[(0, 1.0), (60, 3.0), (120, 2.5), (180, 1.0), (300, 1.0)]    # es decir amplifiquemos los amarillos y verdes y mantenenmos lo demas
P_atenuacion = [(180, 1.0), (240, 0.1), (300, 1.0), (60, 0.2)]          # atenuamos los azules y amarillos, mantenemos lo demas
P_mixto = [(0, 1.8), (60, 0.5), (120, 2.0), (180, 2.0), (300, 1.0)]     # aumentamos rojos verdes y cianes, atenuamos amarillos, mantenemos  magentas



# Con la siguiente función se grafican las curvas de m(h) para cada conjunto de puntos de control definido.
def graficar_curvas_mh(P, titulo, ax):
    # Desempaquetar el conjunto
    h_ctrl = np.array([p[0] for p in P], dtype=float)
    m_ctrl = np.array([p[1] for p in P], dtype=float)
    
    # ordenamos la lista (ya viene ordenada, pero se añade para casos mas generales)
    idx = np.argsort(h_ctrl)
    h_ctrl, m_ctrl = h_ctrl[idx], m_ctrl[idx]
    
    # Generamos ejes y valores
    h_vals = np.linspace(0, 360, 500)
    m_vals = np.interp(h_vals, h_ctrl, m_ctrl, period=360.0)
    
    # Graficar
    ax.plot(h_vals, m_vals, label="Interpolación m(h)", color='black')
    ax.scatter(h_ctrl, m_ctrl, color='red', zorder=5, label="Puntos de control")
    
    
    # Formato
    ax.set_title(titulo)
    ax.set_xlabel("Tono (Grados)")
    ax.set_ylabel("Magnitud (m)")
    ax.set_xlim(0, 360)
    ax.set_ylim(0, max(3.0, max(m_ctrl) + 0.5))
    


# Llamamos a la función: 
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
graficar_curvas_mh(P_aumento, "Aumento Selectivo (Amarillos y Verdes)", axes[0])
graficar_curvas_mh(P_atenuacion, "Atenuación Selectiva (Amarillos y Azules)", axes[1])
graficar_curvas_mh(P_mixto, "Combinación Mixta", axes[2])

plt.tight_layout()
plt.show()


