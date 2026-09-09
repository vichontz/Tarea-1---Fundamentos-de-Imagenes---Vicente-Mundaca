import numpy as np
import matplotlib.pyplot as plt

def rgb_to_hsl(img: np.ndarray) -> np.ndarray:

  img = img.astype(np.float64)
  img = img/ 255.0

  R = img[:, :, 0]
  G = img[:, :, 1]
  B = img[:, :, 2]

  # Se define un epsilon pensando en caso borde de imagen negra
  epsilon = 1e-10

  # Se definen los C y delta
  C_max = np.maximum(np.maximum(R, G), B)
  C_min = np.minimum(np.minimum(R, G), B)
  delta = C_max - C_min

  # L es el promedio entre el máximo y el mínimo
  L = (C_max + C_min) / 2.0

  # S se normaliza por el ancho del rango disponible a esa luminosidad
  den = 1.0 - np.abs(2.0 * L -1.0)
  S = np.where(delta > epsilon, delta / (den + epsilon), 0.0)

  # Para el cálculo de H se define una matriz a "rellenar"
  H = np.zeros_like(C_max)

  # De acuerdo con el canal dominante por pixel creamos mascaras booleanas

  mask_r = (C_max == R) * (delta > epsilon)
  mask_g = (C_max == G) * (delta > epsilon)
  mask_b = (C_max == B) * (delta > epsilon)

  # Se define la fórmula correspondiente por color dominante

  H[mask_r] = 60.0 * (((G[mask_r] - B[mask_r]) / delta[mask_r]) % 6)
  H[mask_g] = 60.0 * (((B[mask_g] - R[mask_g]) / delta[mask_g]) + 2)
  H[mask_b]= 60.0 * (((R[mask_b] - G[mask_b]) / delta[mask_b]) + 4)

  #Si algún grado quedo menor a 0 sumamos 360°

  H = np.where(H < 0, H + 360.0, H)

  #Para zonas grises
  H = np.where(delta < epsilon, 0.0, H)

  hsl_img = np.stack([H, S, L], axis=-1)
  return hsl_img


def plot_hsl(hsl_img: np.ndarray):

  H = hsl_img[:, :, 0]
  S = hsl_img[:, :, 1]
  L = hsl_img[:, :, 2]

  fig, axes = plt.subplots(1, 3, figsize=(15, 5))

  canales = [
      (H, "Hue (H)", "hsv", 0, 360),
      (S, "Saturation (S)", "Reds", 0, 1),
      (L, "Lightness (L)", "gray", 0, 1)
  ]

  for ax, (canal, titulo, cmap, vmin, vmax) in zip(axes, canales):
    im = ax.imshow(canal, cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_title(titulo)
    ax.axis("off")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

  fig.tight_layout()
  #plt.show()