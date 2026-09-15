import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from skimage import exposure
from skimage.io import imread

from Pregunta_1.RGB2HSL import rgb_to_hsl, hsl_to_rgb
from Implementacion import ecualizacion



if __name__ == "__main__":
    img1_path = Path(__file__).resolve().parent / "P2_IMG_2423.tif"
    img1 = imread(img1_path)
    if img1.shape[-1] == 4:
        img1 = img1[:, :, :3]
        
    M_img, N_img = img1.shape[:2]

    # Separación de canales de color
    hsl_img = rgb_to_hsl(img1)
    H = hsl_img[:, :, 0]
    S = hsl_img[:, :, 1]
    L = hsl_img[:, :, 2]  # L está en rango [0.0, 1.0]

    # Evaluación del conjunto E_global
    L_global_8bit = ecualizacion(L, M_img, N_img, alpha=0, clip=0)
    img_global = hsl_to_rgb(H, S, L_global_8bit / 255.0)

    # Evaluación del conjunto E_local
    Hr_loc, Wr_loc = M_img // 8, N_img // 8
    L_local_8bit = ecualizacion(L, Hr_loc, Wr_loc, alpha=0, clip=0)
    img_local_libre = hsl_to_rgb(H, S, L_local_8bit / 255.0)

    # Evaluación del conjunto E_limitado
    L_propuesta_8bit = ecualizacion(L, Hr_loc, Wr_loc, alpha=0, clip=3.0)
    img_propuesta = hsl_to_rgb(H, S, L_propuesta_8bit / 255.0)

    # Comparación con implementación externa CLAHE
    # Se utiliza clip_limit=0.03 como un equivalente estándar normalizado
    L_clahe = exposure.equalize_adapthist(L, kernel_size=(Hr_loc, Wr_loc), clip_limit=0.03)
    img_clahe_ref = hsl_to_rgb(H, S, L_clahe)

    # Renderizado de los resultados
    fig, axes = plt.subplots(1, 5, figsize=(22, 5))
    titulos = ["Original", "Global Clásica", "Local No Limitada", "Propuesta Limitada", "CLAHE Referencia"]
    imagenes = [img1, img_global, img_local_libre, img_propuesta, img_clahe_ref]

    for ax, imagen, titulo in zip(axes, imagenes, titulos):
        # Aseguramos que la imagen esté recortada al rango válido de visualización
        img_visual = np.clip(imagen, 0, 1) if imagen.dtype != np.uint8 else imagen
        ax.imshow(img_visual)
        ax.set_title(titulo)
        ax.axis('off')

    plt.tight_layout()
    plt.show()