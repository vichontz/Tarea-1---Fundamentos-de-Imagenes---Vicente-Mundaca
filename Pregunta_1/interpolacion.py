def interpolacion(h1,h2):
    """
    Interpolación lineal entre dos angulos h1 y h2.
    """
    if h1 > h2:
        h1, h2 = h2, h1
        if h1 + 180 <= h2:          # con estos ifs aseguramos que la interpolación 
            m = (h1+h2)/2           #  sea circular y tome el camino mas corto
        else:
            m = (h1+h2+360)/2
            if m >= 360:
                m -= 360
    return m