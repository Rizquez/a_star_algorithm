# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS / APIs NECESARIAS
# -------------------------------------------------------------------------------------------------------------------------------------------------
import pygame
from ..config.config import ROWS, WHITE, WINDOW_WIDTH, GAP_GRID, GREY
from ..models.point import Point
# -------------------------------------------------------------------------------------------------------------------------------------------------

def create_grid():
    """
    Apply:
    ------
    Metodo encargado de instanciar una lista con las dimenensiones de la red de cuadriculas para la ventana del juego.

    Parameters:
    -----------
    - None.

    Returns:
    --------
    - Lista de listas anidadas con las dimensiones de la red de cuadriculas.
    """
    # Primero vamos a instanciar la lista que va a almacenar 
    # los datos sobre las dimensiones de la red de cuadriculas
    grid = []

    # Ahora vamos a iterar sobre la cantidad filas (la cual por defecto son la misma cantidad de columnas)
    # para crear las dimensiones de la red de cuadriculas
    for row in range(ROWS):
        grid.append([])
        for column in range(ROWS):
            point = Point(row, column)
            grid[row].append(point)

    return grid


def draw_network(window, grid):
    """
    Apply:
    ------
    Metodo encargado de dibujar la red de cuadriculas sobre la ventana que se ha definido previamente.

    Parameters:
    -----------
    window: `pygame.display`
        Objeto de la clase de `pygame` mediante la cual se instancia la ventana mediante la aplicacion del metodo `set_mode`.
    
    grid: `list`
        Lista de listas anidadas con las dimensiones de la red de cuadriculas.

    Returns:
    --------
    - None.
    """
    # Primero definimos el color de la ventana 
    window.fill(WHITE)
    
    # Ahora vamos a iterar sobre la lista con los datos de la red de cuadriculas
    # Y por cada sublista vamos a capturar el punto que ha sido creado para dibujarlo
    # aplicando el metodo interno de la clase que gestiona los punto.
    for row in grid:
        for point in row:
            point.drawing(window)

    # Una vez dibujado cada punto vamos a delinear los contornos para separalos visualmente
    # Al finalizar necesitaremos actualizar la ventana
    draw_squares(window)
    pygame.display.update()


def draw_squares(window):
    """
    Apply:
    ------
    Metodo encargado de delinar las cuadriculas existentes en la ventana.

    Parameters:
    -----------
    window: `pygame.display`
        Objeto de la clase de `pygame` mediante la cual se instancia la ventana mediante la aplicacion del metodo `set_mode`.

    Returns:
    --------
    - None.
    """
    # Constante para indicar la coordenada de inicio de la linea
    START_POINT = 0

    # Ahora simplemente vamos a iterar sobre la cantidad de filas para delinear los bordes de cada cuadricula
    for row in range(ROWS):
        pygame.draw.line(window, GREY, (START_POINT, row * GAP_GRID), (WINDOW_WIDTH, row * GAP_GRID))
        for column in range(ROWS):
            pygame.draw.line(window, GREY, (column * GAP_GRID, START_POINT), (column * GAP_GRID, WINDOW_WIDTH))

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------