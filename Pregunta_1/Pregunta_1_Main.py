import skimage
import numpy as np
import matplotlib.pyplot as plt
from skimage import data
from skimage.io import imsave


from RGB2HSL import rgb_to_hsl, plot_hsl 
from RGB2Lch import rgb_to_lch, plot_lch


imagen_ejemplo = data.astronaut()
imagen_ejemplo2 = imagen_ejemplo.copy()


test = rgb_to_hsl(imagen_ejemplo)
plot_hsl(test)

test2= rgb_to_lch(imagen_ejemplo2)
plot_lch(test2)


def color_saturation( img, h_i, m_i, param):
    """
    Función que ajusta la saturación de una imagen en el espacio de color param.
    
    Entradas:
    img:        Imagen de entrada en formato RGB.
    (h_i, m_i): Conjunto arbitrario de puntos de control.
    param:      parámetro que selecciona el espacio de color utilizado (HSL, lch).
    
    Salidas:
    img_saturada: Imagen con la saturación ajustada.
    """
    return


