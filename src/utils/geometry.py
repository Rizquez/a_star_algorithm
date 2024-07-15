# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS / APIs NECESARIAS
# -------------------------------------------------------------------------------------------------------------------------------------------------
from ..config.config import GAP_GRID
# -------------------------------------------------------------------------------------------------------------------------------------------------

def distance_between_points(point1, point2):
    """
    Apply:
    ------
    Metodo para obtener la distancia entre dos puntos.

    Parameters:
    -----------
    point1: `tuple`
        Coordenadas `xy` del primero punto.
    
    point2: `tuple`
        Coordenadas `xy` del segundo punto.

    Returns:
    --------
    - Distancia calculada entre los puntos recibidos por parametro.
    """
    # Primero extraemos las coordenadas de los puntos para luego calcular y retornar el valor
    x1, y1 = point1
    x2, y2 = point2

    return abs(x1-x2) + abs(y1-y2)

def get_clicked_position(position):
    """
    Apply:
    ------
    Metodo encargado de obtener la fila y columna donde se encuentra posicionado una cuadricula.

    Parameters:
    -----------
    position: `tuple`
        Coordenadas `xy` de la posicion de la cuadricula.

    Returns:
    --------
    - Fila donde esta la cuadricula.
    - Columna donde esta la cuadricula.
    """
    # Extraemos las coordenadas
    y, x = position

    # Ahora necesitamos calcular la fila y columna en funcion de las coordenadas
    row = y // GAP_GRID
    column = x // GAP_GRID
    
    return row, column

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------