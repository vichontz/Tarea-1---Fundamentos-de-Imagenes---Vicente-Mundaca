import numpy as np

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
    return salida.astype(img.dtype)