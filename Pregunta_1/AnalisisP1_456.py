
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread
from pathlib import Path

from ColorSaturation import color_saturation
from AnalisisP1_123 import graficar_curvas_mh

img1_path = Path(__file__).resolve().parent / "P1_IMG_2402.tif"
img1 = imread(img1_path)

img2_path = Path(__file__).resolve().parent / "img2.png"
img2 = imread(img2_path)
if img2.shape[-1] == 4:
    img2 = img2[:, :, :3] 

#para HSL:
#0°  : Rojo
#60° : Amarillo
#120°: Verde
#180°: Cian
#240°: Azul 
#300°: Magenta



# 4)        Explore sistemáticamente la amplitud y el rango de m, la posición y separación de los puntos de 
#           control, y el número de puntos de control. Analice también cómo las decisiones adoptadas en 
#           el diseño de g_m modifican el comportamiento de la herramienta.



P_separados= [(0,1.0), (180, 2.5)]
P_juntos = [(50, 1.0), (55, 2.5), (60, 3.0), (65, 2.5), (70, 1.0)]
P_muchos = [(0, 1.0), (30, 2.0), (60, 3.0), (90, 2.5), (120, 1.5), (150, 1.0), (180, 2.5), (210, 3.0), (240, 2.5), (270, 1.5), (300, 1.0), (330, 2.0)]
P_variantes = [(0, 1.0), (60, 3.0), (120, 0.1), (180, 3.0), (240, 0.1), (300, 1.0)]


fig, axes = plt.subplots(1, 2, figsize=(27, 5))     #Cambiar subplots(1, 2) a subplots(1, 3) para ver tres resultados (muchos/variantes)

graficar_curvas_mh(P_separados, "Puntos Separados", axes[0])
graficar_curvas_mh(P_juntos, "Puntos Juntos", axes[1])
#graficar_curvas_mh(P_muchos, "Puntos Muchos", axes[2])         #Descomentar para ver la figura con muchos puntos
#graficar_curvas_mh(P_variantes, "Puntos Variantes", axes[2])   #Descomentar para ver la figura con puntos variantes

img_separados = color_saturation(img1, P_separados, "LCH")
img_juntos = color_saturation(img1, P_juntos, "LCH")
#img_muchos = color_saturation(img1, P_muchos, "LCH")
#img_variantes = color_saturation(img1, P_variantes, "LCH")

fig, axes = plt.subplots(1, 2, figsize=(27, 7))     #Cambiar subplots(1, 2) a subplots(1, 3) para ver tres resultados (muchos/variantes)
    
axes[0].imshow(img_separados)
axes[0].set_title("Imagen 1 Puntos Separados")
axes[0].axis("off")

axes[1].imshow(img_juntos)
axes[1].set_title("Imagen 1 Puntos Juntos")
axes[1].axis("off")

#axes[2].imshow(img_muchos)                         
#axes[2].set_title("Imagen 1 Puntos Muchos")        # Descomentar para ver la figura con muchos puntos
#axes[2].axis("off")

#axes[2].imshow(img_variantes)                      
#axes[2].set_title("Imagen 1 Puntos Variantes")     # Descomentar para ver la figura con puntos variantes
#axes[2].axis("off")


#5)     Muestre al menos un caso en que una amplificación de saturación o croma produzca una 
#       limitación visible, como clipping, pérdida de detalle cromático o colores difíciles de representar 
#       en RGB. Analice cómo responde su implementación.

P_fiuum = [(0, 1.0), (60, 20.0), (120, 1.0)]        # "Amarillo" exajeradamente amplificado
fig, axes = plt.subplots(1, 3, figsize=(27, 7))

img_fiuum = color_saturation(img1, P_fiuum, "HSL")
img_fiuum2 = color_saturation(img1, P_fiuum, "LCH")

axes[0].imshow(img1)
axes[0].set_title("Imagen 1 Original")
axes[0].axis("off")

axes[1].imshow(img_fiuum)
axes[1].set_title("Amarillo Exagerado (HSL)")
axes[1].axis("off")

axes[2].imshow(img_fiuum2)
axes[2].set_title("Amarillo Exagerado (LCH)")
axes[2].axis("off")

#plt.tight_layout()
#plt.show()  


#6)      Realice al menos una exploración adicional que considere relevante y justifique su elección.

# Tomemos una imagen muy gris e intentemos amplificar los colores para ver si podemos hacerla más vívida. 

#atenuamos con un x100 y amplificamos con un x100, en teoria deberia recuperar la imagen original
P_gris= [(0, 0.01),(180, 0.01)]
P_recuperar = [(0, 100),(180, 100)]


img_gris = color_saturation(img2, P_gris, "HSL")
img_griss = (img_gris.copy() * 255).astype(np.uint8)
img_recuperar = color_saturation(img_griss, P_recuperar, "HSL")

fig, axes = plt.subplots(1, 3, figsize=(27, 5))

axes[0].imshow(img2)
axes[0].set_title("Imagen 2 Original")
axes[0].axis("off")

axes[1].imshow(img_gris)
axes[1].set_title("Imagen 2 gris")
axes[1].axis("off")

axes[2].imshow(img_recuperar)
axes[2].set_title("Imagen 2 recuperada?")
axes[2].axis("off")

plt.tight_layout()
plt.show()