
from pathlib import Path
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
P_mixto = [(0, 0.8), (60, 0.5), (120, 2.0), (180, 2.5), (300, 1.0)]     # aumentamos verdes y cianes, atenuamos rojos y amarillos, mantenemos  magentas



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







# 2)Aplique las configuraciones sobre al menos dos imágenes con características cromáticas diferentes.

# - Testeo con las 2 imagenes solicitadas, se utiliza la imagen P1_IMG_2402.tif, que es la propuesta en ArchivosT1 y img2.png obtenida de internet.

#   - Procesamiento de la imagen 1 -

# Cargar la imagen
img1_path = Path(__file__).resolve().parent / "P1_IMG_2402.tif"
img1 = imread(img1_path)

# Por si viene en RGBA, (no creo)
if img1.shape[-1] == 4:
    img1 = img1[:, :, :3]

# Se procesa la imagen a través de la función de saturación en modo HSL
img_aumento = color_saturation(img1, P_aumento, "HSL")
img_atenuacion = color_saturation(img1, P_atenuacion, "HSL")
img_mixto1 = color_saturation(img1, P_mixto, "HSL")

# Creación de la figura comparativa para el análisis visual
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

axes[0, 0].imshow(img1)
axes[0, 0].set_title("Imagen Original")
axes[0, 0].axis("off")

axes[0, 1].imshow(img_aumento)
axes[0, 1].set_title("Aumento Selectivo (Amarillos y Verdes)")
axes[0, 1].axis("off")

axes[1, 0].imshow(img_atenuacion)
axes[1, 0].set_title("Atenuación Selectiva (Amarillos y Azules)")
axes[1, 0].axis("off")

axes[1, 1].imshow(img_mixto1)
axes[1, 1].set_title("Combinación Mixta")
axes[1, 1].axis("off")

plt.tight_layout()
plt.show()




#   - Procesamiento de la imagen 2 -
img2_path = Path(__file__).resolve().parent / "img2.png"
img2 = imread(img2_path)
if img2.shape[-1] == 4:
    img2 = img2[:, :, :3] 

img_aumento = color_saturation(img2, P_aumento, "HSL")
img_atenuacion = color_saturation(img2, P_atenuacion, "HSL")
img_mixto2 = color_saturation(img2, P_mixto, "HSL")


fig, axes = plt.subplots(2, 2, figsize=(15, 10))

axes[0, 0].imshow(img2)
axes[0, 0].set_title("Imagen Original")
axes[0, 0].axis("off")

axes[0, 1].imshow(img_aumento)
axes[0, 1].set_title("Aumento Selectivo (Amarillos y Verdes)")
axes[0, 1].axis("off")

axes[1, 0].imshow(img_atenuacion)
axes[1, 0].set_title("Atenuación Selectiva (Amarillos y Azules)")
axes[1, 0].axis("off")

axes[1, 1].imshow(img_mixto2)
axes[1, 1].set_title("Combinación Mixta")
axes[1, 1].axis("off")

plt.tight_layout()
plt.show()


# 3)    Compare los modos HS y L*c*h* utilizando mapeos m(h) equivalentes. Analice qué regiones 
#       cambian, cómo cambia su apariencia y por qué los resultados no son necesariamente equivalentes.

#   Sobre "img2.png", mantenemos puntos de control, aplicamos la función de saturación en modo LCH.

img_mixto3 = color_saturation(img1, P_mixto, "LCH")
img_mixto4 = color_saturation(img2, P_mixto, "LCH")

fig, axes = plt.subplots(2, 2, figsize=(15, 10))

axes[0, 0].imshow(img_mixto1)
axes[0, 0].set_title("Imagen 1 HSL")
axes[0, 0].axis("off")

axes[0, 1].imshow(img_mixto3)
axes[0, 1].set_title("Imagen 1 LCH")
axes[0, 1].axis("off")

axes[1, 0].imshow(img_mixto2)
axes[1, 0].set_title("Imagen 2 HSL")
axes[1, 0].axis("off")

axes[1, 1].imshow(img_mixto4)
axes[1, 1].set_title("Imagen 2 LCH")
axes[1, 1].axis("off")

plt.tight_layout()
plt.show()