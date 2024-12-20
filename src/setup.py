# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS / APIs NECESARIAS
# -------------------------------------------------------------------------------------------------------------------------------------------------
import pygame
from .scripts import a_star
from src.models import Point
from settings import ROWS, WHITE, WINDOW_WIDTH, GAP_GRID, GREY
# -------------------------------------------------------------------------------------------------------------------------------------------------

def main_method(window: pygame.Surface) -> None:
    """
    Descripcion
    -----------
    Inicia la aplicacion y gestiona los eventos para el funcionamiento del programa.

    Este metodo principal controla la logica de interaccion del usuario, como dibujar la red de cuadriculas, establecer puntos de inicio y final, 
    marcar barreras y ejecutar el algoritmo A*. Tambien permite reiniciar la red.
    
    Parametros
    ----------
    window
        Ventana de `pygame` utilizada para dibujar y mostrar la red de cuadriculas.
    """
    # Instanciamos los valores inicialres para el inicio, fin y el parametro de control de ejecucion
    start, end, run = None, None, True

    # Ahora vamos a crear la cuadricula que contendra la red de cuadros
    grid = _create_grid()

    # Ahora iniciamos la activacion de los procesos mediante un bucle
    while run:

        # Primero vamos a dibujar todas las cuadriculas de la red
        _draw_network(window, grid)

        # Una vez dibujado necesitamos iterar sobre los eventes que se generen en la ventana
        for event in pygame.event.get():

            # El primer evento en controlar sera la salida del juego
            if event.type == pygame.QUIT:
                run = False

            # Ahora necesitamos verificar si se pulsa la tecla izquierda del raton
            if pygame.mouse.get_pressed()[0]:

                # Para este caso vamos a localizar la posicion donde se dio clic
                # Sobre dicha posicion localizaremos la cuadricula y marcaremos los puntos segun las caracteristicas de cada uno
                position = pygame.mouse.get_pos()
                row, column = _get_clicked_position(position)
                point = grid[row][column]

                # Es importante señalar que siempre el primer clic sera 
                # tomado como punto de inicio, el segundo clic sera tomado 
                # como punto final y todos los demas clic seran las barreras 
                # entre el punto de inicio y el final

                # Si el punto de inicio no esta marcado
                if not start and point != end:
                    start = point
                    start.mark_start()

                # Si el punto de final no esta marcado
                elif not end and point != start:
                    end = point
                    end.mark_end()

                # Sobre los punto de las barreras
                else:
                    point.mark_barrier()

            # Ahora vamos a verificar si se esta pulsando el clic derecho del raton
            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, column = _get_clicked_position(position)
                point = grid[row][column]
                point.reset()

                # Reiniciando los valores del punto de inicio
                if point == start:
                    start = None

                # Reiniciando los valores del punto final
                elif point == end:
                    end = None

            # Ahora la idea seria evaluar el evento que da inicio a la 
            # ejecucion del algoritmo y que reinicia la red de cuadriculas
            # Para manejar estos eventos, nos centraremos en las teclas
            if event.type == pygame.KEYDOWN:

                # El primer evento en controlar sera el de ejecucion del algoritmo
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for point in row:
                            point.update_neighbors(grid)

                    # Una vez actualizamos todos los vecinos, llamamos al algoritmo de la estrella
                    a_star(lambda: _draw_network(window, grid), grid, start, end)

                # Y Ahora para controlar el reinicio usaremos la tacla `C`
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = _create_grid()

    # Por ultimo cerramos la aplicacion
    pygame.quit()

def _get_clicked_position(position: tuple) -> tuple[int, int]:
    """
    Descripcion
    -----------
    Obtiene la fila y columna donde se encuentra un clic en la red de cuadriculas.

    Parametros
    ----------
    position
        Coordenadas `(x, y)` del clic del usuario.

    Retorna
    -------
    - Fila y columna donde se realizo el clic.
    """
    # Extraemos las coordenadas
    y, x = position

    # Ahora necesitamos calcular la fila y columna en funcion de las coordenadas
    row = y // GAP_GRID
    column = x // GAP_GRID
    
    return row, column

def _create_grid() -> list:
    """
    Descripcion
    -----------
    Crea la red de cuadriculas utilizada en el programa.

    Esta funcion genera una lista bidimensional que representa las filas y columnas de la cuadricula.

    Retorna
    -------
    - Lista de listas anidadas con objetos `Point` que representan cada celda de la cuadricula.
    """
    # Primero vamos a instanciar la lista que va a almacenar los datos sobre las dimensiones de la red de cuadriculas
    grid = []

    # Ahora vamos a iterar sobre la cantidad filas (la cual por defecto son la misma cantidad de columnas) para crear 
    # las dimensiones de la red de cuadriculas
    for row in range(ROWS):
        grid.append([])
        for column in range(ROWS):
            point = Point(row, column)
            grid[row].append(point)

    return grid

def _draw_network(window: pygame.Surface, grid: list) -> None:
    """
    Descripcion
    -----------
    Dibuja la red de cuadriculas en la ventana.

    Parametros
    ----------
    window
        Ventana de `pygame` utilizada para dibujar y mostrar la red de cuadriculas.
    
    grid
        Lista de listas anidadas que representa la cuadricula.
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
    _draw_squares(window)
    pygame.display.update()

def _draw_squares(window: pygame.Surface) -> None:
    """
    Descripcion
    -----------
    Dibuja las lineas de las cuadriculas en la ventana.

    Parametros
    ----------
    window
        Ventana de `pygame` utilizada para dibujar y mostrar la red de cuadriculas.
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