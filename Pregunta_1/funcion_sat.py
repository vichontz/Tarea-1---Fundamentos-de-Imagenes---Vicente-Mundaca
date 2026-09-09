def g (S, m_array, mode):
    import numpy as np

    if   mode == "HSL":
        return np.clip (S * m_array, 0, 1.0)
    
    elif mode == "LCH":
        return np.clip (S*m_array,0, None)
    
    else: 
        raise ValueError(("El modo debe ser 'HSL' o 'LCH'") )



