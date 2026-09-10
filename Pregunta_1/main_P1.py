import matplotlib.pyplot as plt
import numpy as np
import cv2
from skimage.io import imsave
from pathlib import Path



#Construya y grafique al menos tres configuraciones distintas de puntos de control, incluyendo 
#una que aumente selectivamente un intervalo de tonos, una que atenúe otro intervalo y una 
#que combine aumentos y disminuciones en distintos tonos.

#hay q definir 3 conjuntos de puntos de control (hI,mi).

#para HSL:
#0°  : Rojo
#60° : Amarillo
#120°: Verde
#180°: Cian
#240°: Azul 
#300°: Magenta
P_aumento =[(60, 1.0), (120, 2.5), (180, 1.0), (300, 1.0)]           # es decir amplifiquemos los verdes y mantenenmos lo demas
P_atenuacion = [(180, 1.0), (240, 0.1), (300, 1.0), (60, 1.0)]      # atenuamos los azules y mantenemos lo demas
P_mixto = [(0, 1.8), (60, 1.8), (120, 1.0), (240, 0.0), (300, 1.0)] # aumentamos rojos y amarillos, atenuamos azules, mantenemos verdes y magentas


