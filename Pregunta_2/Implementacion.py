
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
 