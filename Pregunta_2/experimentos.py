
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from skimage import exposure, color
from skimage.io import imread
from Implementacion import ecualizacion
import time





img1_path = Path(__file__).resolve().parent / "P2_IMG_2423.tif"
img1 = imread(img1_path)
if img1.shape[-1] == 4:
    img1 = img1[:, :, :3]  
img1_f = img1.astype(np.float64)
img1_f = (img1_f - img1_f.min()) / (img1_f.max() - img1_f.min())
img_g = np.round(color.rgb2gray(img1_f) * 255).astype(np.uint8)


img2_path = Path(__file__).resolve().parent / "img2.2.png"
img2 = imread(img2_path)
if img2.shape[-1] == 4:
    img2 = img1[:, :, :3]
img2_f = img2.astype(np.float64)
img2_f = (img2_f - img2_f.min()) / (img2_f.max() - img2_f.min())
img_g2 = np.round(color.rgb2gray(img2_f) * 255).astype(np.uint8)

M, N = img_g.shape


def ecualizacion_global_directa(img):

    hist, _ = np.histogram(img.flatten(),bins=256,range=(0, 256))

    cdf = hist.cumsum()
    cdf_min = cdf[cdf > 0].min()
    cdf_norm = np.round((cdf - cdf_min) * 255 /(cdf.max() - cdf_min))

    return cdf_norm[img].astype(np.uint8)

if __name__ == "__main__":
    print("escriba el numero del experimento que quiera ver (1, 2, 3, 4, 5, 6, 7, u 8)")
   
    accion = int(input())

    M, N = img_g.shape
    Hr_base = M // 8
    Wr_base = N // 8


#   ----    Codigo Experimento 2.1 Ec Global:   ----    
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




#   ----    Codigo Experimento 2.2  tamaño de las regiones y overleap:   ----


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


#   ----    Codigo Experimento 2.3  cantidad de bins:   ----    
    elif accion == 3:
        bins_lista = [ 16, 64, 128, 256]
        tamaños = [32, 128, Wr_base]

        for tamano in tamaños:
            resultados = []
            titulos = []

            for bins in bins_lista:
                resultado = ecualizacion(img_g, Hr=tamano, Wr=tamano, alpha=0.5, clip=0, bins=bins)
                resultados.append(resultado)
                titulos.append(f"{bins} bins")

            fig, axes = plt.subplots(1, len(resultados), figsize=(20, 4))

            for ax, imagen, titulo in zip(axes, resultados, titulos):
                ax.imshow(imagen, cmap="gray", vmin=0, vmax=255)
                ax.set_title(titulo)
                ax.axis("off")

            plt.suptitle(f"Exp 2.3 - Número de bins, región {tamano}x{tamano}")
            plt.tight_layout()
            plt.show()


#   ----    Codigo Experimento 2.4  control de contraste:   ----    
    elif accion == 4:
        clips = [ 5, 10, 20, 50, 0]
        resultados = []
        titulos = []

        for clip in clips:
            resultado = ecualizacion(img_g, Hr=64, Wr=64, alpha=0.5, clip=clip, bins=256)
            resultados.append(resultado)
            titulos.append(f"clip = {clip}")

        fig, axes = plt.subplots(1, len(resultados), figsize=(22, 4))

        for ax, imagen, titulo in zip(axes, resultados, titulos):
            ax.imshow(imagen, cmap="gray", vmin=0, vmax=255)
            ax.set_title(titulo)
            ax.axis("off")

        plt.suptitle("Exp 2.5 - Control de contraste")
        plt.tight_layout()
        plt.show()

#   ----    Codigo Experimento 2.5  Comparación con CLAHE:   ----   

    elif accion == 5:
        imagenes = [("Imagen 1", img_g), ("Imagen 2", img_g2)]
        configuraciones = [(32, 0.10), (64, 0.10), (128, 0.10)]

        for nombre, img in imagenes:
            for tamano, clip_clahe in configuraciones:
                propia = ecualizacion(img, Hr=tamano, Wr=tamano, alpha=0.5, clip=10, bins=256)
                clahe = exposure.equalize_adapthist(img, kernel_size=(tamano, tamano), clip_limit=clip_clahe)
                clahe = np.round(clahe * 255).astype(np.uint8)

                fig, axes = plt.subplots(1, 3, figsize=(15, 5))
                axes[0].imshow(img, cmap="gray", vmin=0, vmax=255)
                axes[0].set_title("Original")
                axes[1].imshow(propia, cmap="gray", vmin=0, vmax=255)
                axes[1].set_title("Método propio")
                axes[2].imshow(clahe, cmap="gray", vmin=0, vmax=255)
                axes[2].set_title("CLAHE")

                for ax in axes:
                    ax.axis("off")

                plt.suptitle(f"{nombre} - Región {tamano}x{tamano}")
                plt.tight_layout()
                plt.show()


#   ----    Codigo Experimento 2.6  Caso no deseado:   ----   
    elif accion == 6:
        local_sin_limite = ecualizacion(img_g, Hr=32, Wr=32, alpha=0.5, clip=0, bins=256)
        local_limitada = ecualizacion(img_g, Hr=32, Wr=32, alpha=0.5, clip=2, bins=256)

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        axes[0].imshow(img_g, cmap="gray", vmin=0, vmax=255)
        axes[0].set_title("Original")
        axes[1].imshow(local_sin_limite, cmap="gray", vmin=0, vmax=255)
        axes[1].set_title("Local sin límite")
        axes[2].imshow(local_limitada, cmap="gray", vmin=0, vmax=255)
        axes[2].set_title("Local limitada")

        for ax in axes:
            ax.axis("off")

        plt.suptitle("Exp 2.7 - Caso problemático")
        plt.tight_layout()
        plt.show()


#   ----    Codigo Experimento 2.7  discontinuidades y artefactos:   ----   
    elif accion == 7:
        sin_overlap = ecualizacion(img_g, Hr=Hr_base, Wr=Wr_base, alpha=0, clip=0, bins=256)
        con_overlap = ecualizacion(img_g, Hr=Hr_base, Wr=Wr_base, alpha=0.7, clip=0, bins=256)
        recorte = (slice(Hr_base-100,Hr_base+100), slice(Wr_base-40, Wr_base+40))
        imagenes = [img_g[recorte], sin_overlap[recorte], con_overlap[recorte]]
        titulos = ["Original", "α = 0", "α = 0.5"]

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        for ax, imagen, titulo in zip(axes, imagenes, titulos):
            ax.imshow(imagen, cmap="gray", vmin=0, vmax=255)
            ax.set_title(titulo)
            ax.axis("off")

        plt.suptitle("Exp 2.8 - Artefactos en fronteras")
        plt.tight_layout()
        plt.show()


#   ----    Codigo Experimento 2.8  Exploración adicional:   ----   
    #elif accion == 8:
        tamanos = [16, 32, 64, 128, 256]
        tiempos = []

        for tamano in tamanos:
            inicio = time.perf_counter()
            ecualizacion(img_g, Hr=tamano, Wr=tamano, alpha=0.5, clip=0, bins=256)
            fin = time.perf_counter()
            tiempos.append(fin - inicio)

        plt.figure(figsize=(8, 5))
        plt.plot(tamanos, tiempos, marker="o")
        plt.xlabel("Tamaño de región")
        plt.ylabel("Tiempo [s]")
        plt.title("Exp 2.9 - Costo computacional")
        plt.grid()
        plt.tight_layout()
        plt.show()
