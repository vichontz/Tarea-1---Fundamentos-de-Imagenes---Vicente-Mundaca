import numpy as np
from skimage import data 
def reescalar_imagen(img, s, modo="bilineal"):
    H_in, W_in = img.shape[:2]

    # Tamaño de salida definido por redondeo
    H_out = round(H_in * s)
    W_out = round(W_in * s)

    # Convertimos a float64 para evitar desbordamientos en la matemática
    img_f = img.astype(np.float64)

    # Crear matrices de coordenadas para toda la imagen
    j, i = np.meshgrid(np.arange(W_out), np.arange(H_out))

    # Mapeo inverso
    y = i / s
    x = j / s

    if modo == "vecino":
        # Redondeo y clamping 
        yi = np.clip(np.round(y).astype(int), 0, H_in - 1)
        xi = np.clip(np.round(x).astype(int), 0, W_in - 1)
        salida = img_f[yi, xi]

    else:  # bilineal
        # Cálculo de los cuatro vértices enteros para cada píxel simultáneamente
        y0 = np.floor(y).astype(int)
        x0 = np.floor(x).astype(int)
        y1 = y0 + 1
        x1 = x0 + 1

        # Matrices de pesos fraccionarios
        wy = y - y0
        wx = x - x0

        # Si la imagen es RGB (3 dimensiones), adaptamos las matrices de 
        # pesos (2D) añadiendo un eje vacío para que NumPy pueda multiplicarlas
        if img.ndim == 3:
            wy = wy[..., np.newaxis]
            wx = wx[..., np.newaxis]

        # Casos borde
        y0c = np.clip(y0, 0, H_in - 1)
        y1c = np.clip(y1, 0, H_in - 1)
        x0c = np.clip(x0, 0, W_in - 1)
        x1c = np.clip(x1, 0, W_in - 1)

        # Obtenemos vecinitos
        p00 = img_f[y0c, x0c]
        p01 = img_f[y0c, x1c]
        p10 = img_f[y1c, x0c]
        p11 = img_f[y1c, x1c]

        # Interpolación bilineal
        arriba = p00 * (1 - wx) + p01 * wx
        abajo = p10 * (1 - wx) + p11 * wx
        salida = arriba * (1 - wy) + abajo * wy

    # Recorte final y restauración del tipo de dato original
    salida = np.clip(salida, 0, 255)
    return np.round(salida).astype(img.dtype)


#Testeo para un pixel:
img = data.camera() #imagen random
s = 1.37
H_in, W_in = img.shape

i, j = 200, 340

y = i / s
x = j / s
y0, x0 = int(np.floor(y)), int(np.floor(x))
y1, x1 = y0 + 1, x0 + 1
wy, wx = y - y0, x - x0

y0c, y1c = min(y0, H_in-1), min(y1, H_in-1)
x0c, x1c = min(x0, W_in-1), min(x1, W_in-1)

p00 = float(img[y0c, x0c]); p01 = float(img[y0c, x1c])
p10 = float(img[y1c, x0c]); p11 = float(img[y1c, x1c])

arriba = p00*(1-wx) + p01*wx
abajo  = p10*(1-wx) + p11*wx
valor  = arriba*(1-wy) + abajo*wy

out = reescalar_imagen(img, s, modo='bilineal')

print(f'Trazado de un pixel, s={s}, modo bilineal')
print(f'Coordenada salida           : (i,j) = ({i}, {j})')
print(f'Coordenada entrada          : (y,x) = ({y:.3f}, {x:.3f})')
print(f'Vecino arriba-izq           : ({y0},{x0}) = {p00}')
print(f'Vecino arriba-der           : ({y0},{x1}) = {p01}')
print(f'Vecino abajo-izq            : ({y1},{x0}) = {p10}')
print(f'Vecino abajo-der            : ({y1},{x1}) = {p11}')
print(f'Pesos                       : wy = {wy:.3f}, wx = {wx:.3f}')
print(f'Interpolacion horizontal    : arriba = {arriba:.3f}, abajo = {abajo:.3f}')
print(f'Valor interpolado final     : {valor:.3f} redondeado = {int(np.clip(round(valor),0,255))}')
print(f'Valor real [{i},{j}]: {out[i,j]} ')
