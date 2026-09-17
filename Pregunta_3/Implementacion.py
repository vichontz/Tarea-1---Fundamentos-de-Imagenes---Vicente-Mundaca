import numpy as np

def reescalar_imagen(img, s, modo="bilineal"):
    
    H_in, W_in = img.shape[0], img.shape[1]

    # Tamano de salida: H_in*s y W_in*s no siempre dan un entero exacto.
    # Se define explicitamente: se redondea al entero mas cercano.
    H_out = round(H_in * s)
    W_out = round(W_in * s)

    if img.ndim == 3:
        salida = np.zeros((H_out, W_out, img.shape[2]), dtype=np.float64)
    else:
        salida = np.zeros((H_out, W_out), dtype=np.float64)

    img_f = img.astype(np.float64)

    for i in range(H_out):
        for j in range(W_out):
            y = i / s
            x = j / s

            if modo == "vecino":

                yi = min(round(y), H_in - 1)
                xi = min(round(x), W_in - 1)
                salida[i, j] = img_f[yi, xi]

            else:  # bilineal
    
                y0 = int(np.floor(y))
                x0 = int(np.floor(x))
                y1 = y0 + 1
                x1 = x0 + 1

                wy = y - y0
                wx = x - x0

                y0c = min(max(y0, 0), H_in - 1)
                y1c = min(max(y1, 0), H_in - 1)
                x0c = min(max(x0, 0), W_in - 1)
                x1c = min(max(x1, 0), W_in - 1)

                p00 = img_f[y0c, x0c]   # arriba-izquierda
                p01 = img_f[y0c, x1c]   # arriba-derecha
                p10 = img_f[y1c, x0c]   # abajo-izquierda
                p11 = img_f[y1c, x1c]   # abajo-derecha

                arriba = p00 * (1 - wx) + p01 * wx
                abajo = p10 * (1 - wx) + p11 * wx
                salida[i, j] = arriba * (1 - wy) + abajo * wy

    salida = np.clip(salida, 0, 255)
    return salida.astype(img.dtype)


