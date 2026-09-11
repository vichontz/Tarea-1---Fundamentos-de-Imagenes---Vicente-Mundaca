
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




# 4)        Explore sistemáticamente la amplitud y el rango de m, la posición y separación de los puntos de 
#           control, y el número de puntos de control. Analice también cómo las decisiones adoptadas en 
#           el diseño de g_m modifican el comportamiento de la herramienta.

P_separados= [(0,1.0), (180, 2.5)]
P_juntos = [(110,1.0), (120, 2.5), (130, 1.0)]

fig, axes = plt.subplots(1, 2, figsize=(18, 5))
graficar_curvas_mh(P_separados, "Puntos Separados", axes[0])
graficar_curvas_mh(P_juntos, "Puntos Juntos", axes[1])
         

img_separados = color_saturation(img1, P_separados, "LCH")
img_juntos = color_saturation(img1, P_juntos, "LCH")
fig, axes = plt.subplots(1, 2, figsize=(15, 7))

axes[0].imshow(img_separados)
axes[0].set_title("Imagen 1 Puntos Separados")
axes[0].axis("off")

axes[1].imshow(img_juntos)
axes[1].set_title("Imagen 1 Puntos Juntos")
axes[1].axis("off")


plt.tight_layout()
plt.show()  