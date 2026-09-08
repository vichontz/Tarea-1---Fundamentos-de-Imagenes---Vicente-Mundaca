from skimage import color
import numpy as np
import matplotlib.pyplot as plt
def rgb_to_lch(img: np.ndarray) -> np.ndarray:

    lab = color.rgb2lab(img)

    L = lab[:, :, 0]
    a = lab[:, :, 1]
    b = lab[:, :, 2]

    C = np.sqrt(a ** 2 + b ** 2)
    h = np.degrees(np.arctan2(b, a))
    h = np.where(h < 0, h + 360.0, h)

    lch_img = np.stack([L, C, h], axis=-1)
    return lch_img

def plot_lch(lch_img: np.ndarray, figsize=(15, 5)):

    L = lch_img[:, :, 0]
    C = lch_img[:, :, 1]
    h = lch_img[:, :, 2]

    fig, axes = plt.subplots(1, 3, figsize=figsize)

    canales = [
        (L, "L (Lightness)", "gray", 0, 100),
        (C, "C (Chroma)", "magma", C.min(), C.max()),
        (h, "h (hue)", "hsv", 0, 360),
    ]

    for ax, (canal, titulo, cmap, vmin, vmax) in zip(axes, canales):
        im = ax.imshow(canal, cmap=cmap, vmin=vmin, vmax=vmax)
        ax.set_title(titulo)
        ax.axis("off")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    fig.tight_layout()
    plt.show()