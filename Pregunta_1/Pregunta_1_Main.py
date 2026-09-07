import skimage
import numpy as np
import matplotlib.pyplot as plt
from skimage import data
from skimage.io import imsave


from RGB2HSL import rgb_to_hsl, plot_hsl 

imagen_ejemplo = data.astronaut()


test = rgb_to_hsl(imagen_ejemplo)
plot_hsl(test)

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
