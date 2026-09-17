# Exp 2.9 : Efecto de la ecualización local sobre imágenes a color

import numpy as np
import matplotlib.pyplot as plt
from skimage import color
from skimage.io import imread
from pathlib import Path
from Implementacion import ecualizacion


def ecualizar_color(img_rgb, Hr, Wr, alpha, clip):

    # Extraer L
    lab = color.rgb2lab(img_rgb)
    L = lab[:, :, 0]

    # [0,100] a [0,255]
    L_u8 = np.round(L * 255 / 100).astype(np.uint8)

    L_eq = ecualizacion(L_u8, Hr, Wr, alpha, clip)
    
    # [0,255] a [0,100]
    L_eq = L_eq.astype(float) * 100 / 255

    # rearmamos
    lab[:, :, 0] = L_eq
    img_salida = color.lab2rgb(lab)

    return np.clip(img_salida, 0, 1)



# Cargar imagenes
img1_path = Path(__file__).resolve().parent / "P2_IMG_2423.tif"
img1 = imread(img1_path)
if img1.shape[-1] == 4:
    img1 = img1[:, :, :3]  
img1_f = img1.astype(np.float64)
img1 = (img1_f - img1_f.min()) / (img1_f.max() - img1_f.min())



img2_path = Path(__file__).resolve().parent / "img2.2.png"
img2 = imread(img2_path)
if img2.shape[-1] == 4:
    img2 = img1[:, :, :3]
img2_f = img2.astype(np.float64)
img2 = (img2_f - img2_f.min()) / (img2_f.max() - img2_f.min())



# Parámetros
#img = img1
img = img2
Hr = 64
Wr = 64
alpha = 0.5

clips = [ 8, 0]
nombres = [" β = 8","β=0"]


plt.figure(figsize=(16, 4))

plt.subplot(1, 3, 1)
plt.imshow(img)
plt.title("Original")
plt.axis("off")

for i in range(len(clips)):

    resultado = ecualizar_color(img,Hr,Wr,alpha,clips[i])

    plt.subplot(1, 3, i + 2)
    plt.imshow(resultado)
    plt.title(nombres[i])
    plt.axis("off")

plt.suptitle("Ecualización local de luminancia en imagen a color")
plt.tight_layout()
plt.show()
