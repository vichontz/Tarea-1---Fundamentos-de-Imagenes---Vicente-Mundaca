import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

from skimage import exposure, color
from skimage.io import imread

from Implementacion import ecualizacion

if __name__ == "__main__":
    img1_path = Path(__file__).resolve().parent / "P2_IMG_2423.tif"
    img1 = imread(img1_path)
    if img1.shape[-1] == 4:
        img1 = img1[:, :, :3]
        
    img1_f = img1.astype(np.float64)
    img1_f = (img1_f - img1_f.min()) / (img1_f.max() - img1_f.min())

    img_g = np.round(color.rgb2gray(img1_f) * 255).astype(np.uint8)
    M, N = img_g.shape

    Hr, Wr = M // 8, N // 8

    # global:
    img_global = ecualizacion(img_g, M, N, alpha=0, clip=0)

    # local sin solapamiento.
    img_l = ecualizacion(img_g, Hr, Wr, alpha=0, clip=0)

    # local sin solapamiento, con clipeo
    img_clip = ecualizacion(img_g, Hr, Wr, alpha=0, clip=7.0)

    # Comparación externa CLAHE
    img_clahe = exposure.equalize_adapthist(img_g, kernel_size=(Hr, Wr), clip_limit=0.03) # Se utiliza clip_limit=0.03 como un equivalente estándar 
    
    # Renderizado de resultados
    fig, axes = plt.subplots(1, 5, figsize=(22, 5))
    titulos = ["Original", "Global", "Local No Limitada", "Local Limitada", "CLAHE"]
    imagenes = [img_g, img_global, img_l, img_clip, img_clahe]

    for ax, imagen, titulo in zip(axes, imagenes, titulos):
        ax.imshow(imagen, cmap = "gray")
        ax.set_title(titulo)
        ax.axis('off')

    plt.tight_layout()
    plt.show()
