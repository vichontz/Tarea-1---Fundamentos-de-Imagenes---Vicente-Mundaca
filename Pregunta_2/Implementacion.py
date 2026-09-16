
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
    
    return C, centros_y, centros_x, Hr, Wr




def calcular_cdfs(img_gris, C, Hr, Wr, clip_l=0, bins=256):

    cdfs_locales = {}

    if img_gris.dtype != np.uint8:
        if img_gris.max() <= 1.0:
            img_calc = np.round(img_gris * 255).astype(np.uint8)
        else:
            img_calc = img_gris.astype(np.uint8)
    else:
        img_calc = img_gris.copy()

    N_prom = (Hr * Wr) / bins
    limite = clip_l * N_prom

    for y_c, x_c in C:

        x_in = x_c - Wr // 2
        x_fin = x_in + Wr

        y_in = y_c - Hr // 2
        y_fin = y_in + Hr

        parche = img_calc[y_in:y_fin, x_in:x_fin]

        hist, _ = np.histogram(
            parche.flatten(),
            bins=bins,
            range=(0, 256)
        )

        if clip_l > 0:

            exceso = np.maximum(hist - limite, 0).sum()

            hist_clipeado = np.minimum(hist, limite)

            incremento_base = int(exceso // bins)
            hist_clipeado += incremento_base

            resto = int(exceso % bins)

            if resto > 0:
                indices = np.linspace(
                    0,
                    bins - 1,
                    resto,
                    dtype=int
                )

                hist_clipeado[indices] += 1

            hist_usar = hist_clipeado

        else:
            hist_usar = hist

        cdf = hist_usar.cumsum()

        cdf_min = cdf[cdf > 0].min() if cdf.max() > 0 else 0
        rango_cdf = cdf.max() - cdf_min

        if rango_cdf > 0:

            cdf_norm = np.round(
                (cdf - cdf_min) * 255 / rango_cdf
            ).astype(np.uint8)

        else:

            cdf_norm = np.zeros(bins, dtype=np.uint8)

        # Convertir los 256 niveles de intensidad
        # al bin correspondiente
        niveles = np.arange(256)

        indices_bins = np.floor(
            niveles * bins / 256
        ).astype(int)

        indices_bins = np.minimum(indices_bins, bins - 1)

        # LUT de 256 niveles
        lut = cdf_norm[indices_bins]

        cdfs_locales[(y_c, x_c)] = lut

    return cdfs_locales, img_calc


def interpolacion_bilineal(img_calc, cdfs_locales, centros_y, centros_x):
    img_eq = np.zeros_like(img_calc, dtype=np.float32)
    
    # Añadimos los bordes
    y_lim = [0] + centros_y + [img_calc.shape[0]]
    x_lim = [0] + centros_x + [img_calc.shape[1]]
    
    for i in range(len(y_lim) - 1):
        y_ini, y_fin = y_lim[i], y_lim[i+1]
        if y_ini == y_fin: continue # Caso borde 
        
        # Determinar los centros y1, y2 que encierran elbloque
        c_y1 = centros_y[max(0, i - 1)]
        c_y2 = centros_y[min(len(centros_y) - 1, i)]
        
        for j in range(len(x_lim) - 1):
            x_ini, x_fin = x_lim[j], x_lim[j+1]
            if x_ini == x_fin: continue
            
            # lo mismo pero con x
            c_x1 = centros_x[max(0, j - 1)]
            c_x2 = centros_x[min(len(centros_x) - 1, j)]
            
            # obtenemos el bloque inicial
            blq = img_calc[y_ini:y_fin, x_ini:x_fin]
            
            # Recuperación de las 4 distribuciones desde nuestro diccionario
            cdf_11 = cdfs_locales[(c_y1, c_x1)]
            cdf_12 = cdfs_locales[(c_y1, c_x2)]
            cdf_21 = cdfs_locales[(c_y2, c_x1)]
            cdf_22 = cdfs_locales[(c_y2, c_x2)]
            
            # Mapeo simultáneo de todo el bloque 
            v_11 = cdf_11[blq]
            v_12 = cdf_12[blq]
            v_21 = cdf_21[blq]
            v_22 = cdf_22[blq]
            
            
            y_coords = np.arange(y_ini, y_fin)
            if c_y1 == c_y2:  # Borde superior o inferior 
                ty = np.zeros_like(y_coords, dtype=np.float32)
            else:
                ty = (y_coords - c_y1) / (c_y2 - c_y1)
                
            x_coords = np.arange(x_ini, x_fin)
            if c_x1 == c_x2:  # Borde del lado
                tx = np.zeros_like(x_coords, dtype=np.float32)
            else:
                tx = (x_coords - c_x1) / (c_x2 - c_x1)
                
            # Ajuste pa mutiplicar
            TY = ty[:, np.newaxis]
            TX = tx[np.newaxis, :]
            
            # Ec de Interpolación Bilineal  
            interp_y1 = v_11 * (1 - TX) + v_12 * TX
            interp_y2 = v_21 * (1 - TX) + v_22 * TX
            interp_final = interp_y1 * (1 - TY) + interp_y2 * TY
            
            #resultado al arreglo
            img_eq[y_ini:y_fin, x_ini:x_fin] = interp_final
            
    return np.round(img_eq).astype(np.uint8)

            
def ecualizacion(img, Hr, Wr, alpha, clip=0, bins=256):
    M, N = img.shape
    C, centros_y, centros_x, Hr, Wr = generar_malla(M, N, Hr, Wr, alpha)
    cdfs, img_calc = calcular_cdfs(img, C, Hr, Wr, clip, bins)
    return interpolacion_bilineal(img_calc, cdfs, centros_y, centros_x)



