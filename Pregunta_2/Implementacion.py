
import numpy as np 


def generar_malla(M, N, Hr, Wr, alpha):
    # para permitir tomar una malla de tamaño maximo, sin tener que saber las dimensiones exactas de la foto
    Hr = min(Hr, M)
    Wr = min(Wr, N)
    
    # calculo de los saltos, se añade la función max para q si la imagen es pequeña no intente hacer saltos menores a un pixel
    Sy = max(1, int(Hr * (1 - alpha)))
    Sx = max(1, int(Wr * (1 - alpha)))
    
    # coordenadas para el eje y 
    centros_y = list(range(Hr // 2, M - Hr // 2 + 1, Sy))
    if not centros_y or centros_y[-1] != M - Hr // 2:
        centros_y.append(M - Hr // 2)
        
    # coordenadas para el eje x
    centros_x = list(range(Wr // 2, N - Wr // 2 + 1, Sx))
    if not centros_x or centros_x[-1] != N - Wr // 2:
        centros_x.append(N - Wr // 2)
        
    # Creamos las tuplas correspondientes a los centros
    C = [(y_c, x_c) for y_c in centros_y for x_c in centros_x]
    
    return C, centros_y, centros_x




def calcular_cdfs(img_gris, C, Hr, Wr):
    cdfs_locales = {}
    
    # Estandarización a 8 bits para asegurar 256 bins exactos
    if img_gris.dtype != np.uint8:
        if img_gris.max() <= 1.0:
            img_calc = (img_gris * 255).astype(np.uint8)
        else:
            img_calc = img_gris.astype(np.uint8)
    else:
        img_calc = img_gris.copy()

    # Iteración sobre centros
    for y_c, x_c in C:
    
        # Definimos las fronteras
        x_in = x_c - Wr // 2
        x_fin = x_in + Wr
        y_in = y_c - Hr // 2
        y_fin = y_in + Hr
        

        # Creamos el bloque
        parche = img_calc[y_in:y_fin, x_in:x_fin]
        
        # Cálculo del histograma y la Función de Distribución Acumulada
        hist, _ = np.histogram(parche.flatten(), bins=256, range=(0, 256))
        cdf = hist.cumsum()
        
        # Normalización de la CDF al rango de intensidades [0, 255]
        cdf_min = cdf[cdf > 0].min() if cdf.max() > 0 else 0
        rango_cdf = cdf.max() - cdf_min
        
        if rango_cdf > 0:
            cdf_norm = np.round((cdf - cdf_min) * 255 / rango_cdf).astype(np.uint8)
        else:
            # Caso borde (un solo color)
            cdf_norm = np.arange(256, dtype=np.uint8)
            
        # Diccionario usando el centro como key
        cdfs_locales[(y_c, x_c)] = cdf_norm
        
    return cdfs_locales, img_calc