import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from skimage.io import imread
from skimage import exposure, color

from Implementacion import reescalar_imagen




img1_path = Path(__file__).resolve().parent / "P3_IMG_2387.tif"
img1 = imread(img1_path)
if img1.shape[-1] == 4:
    img1 = img1[:, :, :3]  


#img2_path = Path(__file__).resolve().parent / "img2.2.png"
#img2 = imread(img2_path)



if __name__ == "__main__":
    print("escriba el numero del experimento que quiera ver (1, 2, 3, 4, 5, 6, 7, u 8)")
    accion = int(input())

#   ----    Codigo Experimento 3.1 y 3.2 Escalamientos:   ----    
    if accion == 1 or accion == 2:

        img=img1
        factores = [0.51, 0.73, 1.5, 1.99]
        

        plt.figure(figsize=(16, 8))

        for k in range(len(factores)):
           
            s = factores[k]
            recorte = (slice(int(s * 700), int(s * 900)),slice(int(s * 300), int(s * 500))) 
            resultado_vecino = reescalar_imagen(img, s, "vecino")
            resultado_bilineal = reescalar_imagen(img, s, "bilineal")

            plt.subplot(2, len(factores), k + 1)
            if accion == 2:
                plt.imshow(resultado_vecino[recorte], cmap="gray")
            else:
                plt.imshow(resultado_vecino, cmap="gray")
                  
            plt.title("Vecino, s=" + str(s))
            plt.axis("off")

            plt.subplot(2, len(factores), len(factores) + k + 1)
            plt.imshow(resultado_bilineal[recorte], cmap="gray")
            plt.title("Bilineal, s=" + str(s))
            plt.axis("off")

        plt.tight_layout()
        plt.show()
        
#   ----    Codigo Experimento 2.3  tamaño de las regiones y overleap:   ----
    #elif accion == 3:
        
#   ----    Codigo Experimento 2.3  cantidad de bins:   ----    
    #elif accion == 3:
       
#   ----    Codigo Experimento 2.4  control de contraste:   ----    
    #elif accion == 4:
        
    #elif accion == 5:
        
#   ----    Codigo Experimento 2.6  Caso no deseado:   ----   
    #elif accion == 6:
        
#   ----    Codigo Experimento 2.7  discontinuidades y artefactos:   ----   
    #elif accion == 7:
        
#   ----    Codigo Experimento 2.8  Exploración adicional:   ----   
    #elif accion == 8:
        
    #else: