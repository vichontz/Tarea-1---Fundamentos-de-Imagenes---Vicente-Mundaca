
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from skimage import exposure, color
from skimage.io import imread
from Implementacion import ecualizacion




#   ----    Codigo Experimento 2.1 Ec Global:   ----

img1_path = Path(__file__).resolve().parent / "P2_IMG_2423.tif"
img1 = imread(img1_path)
if img1.shape[-1] == 4:
    img1 = img1[:, :, :3]
    
img1_f = img1.astype(np.float64)
img1_f = (img1_f - img1_f.min()) / (img1_f.max() - img1_f.min())

img_g = np.round(color.rgb2gray(img1_f) * 255).astype(np.uint8)
M, N = img_g.shape


def ecualizacion_global_directa(img):

    hist, _ = np.histogram(img.flatten(),bins=256,range=(0, 256))

    cdf = hist.cumsum()
    cdf_min = cdf[cdf > 0].min()
    cdf_norm = np.round((cdf - cdf_min) * 255 /(cdf.max() - cdf_min))

    return cdf_norm[img].astype(np.uint8)

if __name__ == "__main__":
    print("escriba 1 para ver grafico 1 del informe")
    print("escriba 2 para ver grafico 2 del informe")
    accion = int(input())

    M, N = img_g.shape
    Hr_base = M // 8
    Wr_base = N // 8
    if accion == 1:
        

        global_directa = ecualizacion_global_directa(img_g)

        una_region = ecualizacion(img_g,Hr=M,Wr=N,alpha=0,clip=0,bins=256)

        diferencia = np.abs(global_directa.astype(int)- una_region.astype(int))

        print("Diferencia máxima:", diferencia.max())
        print("Diferencia promedio:", diferencia.mean())

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        axes[0].imshow(img_g, cmap="gray", vmin=0, vmax=255)
        axes[0].set_title("Original")

        axes[1].imshow(global_directa, cmap="gray", vmin=0, vmax=255)
        axes[1].set_title("Global directa")

        axes[2].imshow(una_region, cmap="gray", vmin=0, vmax=255)
        axes[2].set_title("Una región")

        for ax in axes:
            ax.axis("off")

        plt.tight_layout()
        plt.show()




#   ----    Codigo Experimento 2.2  tamaño de las regiones:   ----


    elif accion == 2:
        tamaños = [32, 64, 128, 256]

        resultados = [img_g]
        titulos = ["Original"]

        for t in tamaños:

            resultado = ecualizacion(img_g,Hr=t,Wr=t,alpha=0.5,clip=0,bins=256)
            resultados.append(resultado)
            titulos.append(f"Región {t}x{t}")

        fig, axes = plt.subplots(1,len(resultados),figsize=(20, 4))

        for ax, imagen, titulo in zip(axes,resultados,titulos):

            ax.imshow(imagen,cmap="gray",vmin=0,vmax=255)
            ax.set_title(titulo)
            ax.axis("off")

        plt.suptitle("Exp 2.2 - Tamaño de región")
        plt.tight_layout()
        plt.show()
 
        alphas = [0.0, 0.25, 0.5, 0.90]

        resultados = []
        titulos = []

        for alpha in alphas:

            resultado = ecualizacion(img_g,Hr=Hr_base,Wr=Wr_base,alpha=alpha,clip=0,bins=256)
            resultados.append(resultado)
            titulos.append(f"α = {alpha}")

        fig, axes = plt.subplots(1,len(resultados),figsize=(16, 4))

        for ax, imagen, titulo in zip(axes,resultados,titulos):

            ax.imshow(imagen,cmap="gray",vmin=0,vmax=255)
            ax.set_title(titulo)
            ax.axis("off")

        plt.suptitle("Exp 2.2 - Efecto del overlap")
        plt.tight_layout()
        plt.show()


        # Recorte para observar fronteras
        recorte = (slice(430, 580),slice(290, 420))
        fig, axes = plt.subplots(1,len(resultados),figsize=(16, 4))

        for ax, imagen, titulo in zip(axes,resultados,titulos ):

            ax.imshow(imagen[recorte],cmap="gray",vmin=0,vmax=255)
            ax.set_title(titulo)
            ax.axis("off")

        plt.suptitle("Exp 2.2 - Zoom en fronteras")
        plt.tight_layout()
        plt.show()    


#   ----    Codigo Experimento 2.2  tamaño de las regiones:   ----    
    elif accion == 3:
        