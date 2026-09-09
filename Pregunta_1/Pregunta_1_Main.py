import skimage
import numpy as np
import matplotlib.pyplot as plt
from skimage import data
from skimage.io import imsave


from RGB2HSL import rgb_to_hsl, hsl_to_rgb
from RGB2Lch import rgb_to_lch, lch_to_rgb
from funcion_sat import g


def color_saturation( img, puntos, param):
    """
    Función que ajusta la saturación de una imagen en el espacio de color param.
    
    Entradas:
    img:        Imagen de entrada en formato RGB (Array).
    puntos:     Lista de tuplas ej [(h1,m1),(h2,m2),...].
    param:      parámetro que selecciona el espacio de color utilizado (HSL o lCH).
    
    Salidas:
    img_saturada: Imagen con la saturación ajustada [0, 1] en RGB .
    """

    #extraemos dos listas para los puntos de control y las ordenamos
    h_ctrl = np.array([p[0] for p in puntos], dtype=float)
    m_ctrl = np.array([p[1] for p in puntos], dtype=float)
    idx = np.argsort(h_ctrl)
    h_ctrl = h_ctrl[idx]
    m_ctrl = m_ctrl[idx]


    param = param.upper() #porsiaca


    if param == "HSL":

        #pasamos a HSL:
        hsl_img = rgb_to_hsl(img)
        H = hsl_img[:, :, 0]
        S = hsl_img[:, :, 1]
        L_val = hsl_img[:, :, 2]
        
        #  Interpolación periódica:
        m_array = np.interp(H, h_ctrl, m_ctrl, period=360.0)
        
        # Aplicamos g (incluye el recorte [0, 1]).
        S_nueva = g(S, m_array, param)              # nota: no hacia falta definir g aparte, pero puede servir en
                                                    # caso de que se quieran hacer otras funciones de forma limpia
        # pasamos a RGB de HSL:
        hsl_mod = np.stack([H, S_nueva, L_val], axis=-1)
        img_saturada = hsl_to_rgb(hsl_mod)

        return img_saturada

    elif param == "LCH":

        #pasamos a LCH:
        lch_img = rgb_to_lch(img)
        L = lch_img[:, :, 0]
        C = lch_img[:, :, 1]
        h_val = lch_img[:, :, 2]

        #  Interpolación periódica:
        m_array = np.interp(h_val, h_ctrl, m_ctrl, period=360.0)

        # Aplicamos g (incluye el recorte [0, 1]).
        C_nueva = g(C, m_array, param)             
                                                    
        # pasamos a RGB de LCH:
        lch_mod = np.stack([L, C_nueva, h_val], axis=-1)
        img_saturada = lch_to_rgb(lch_mod)

        return img_saturada
    else:
        raise ValueError("El parámetro 'param' debe ser 'HSL' o 'LCH'")


