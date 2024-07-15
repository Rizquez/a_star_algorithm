# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS / APIs NECESARIAS
# -------------------------------------------------------------------------------------------------------------------------------------------------
import pygame
from .utils.drawing import create_grid, draw_network
from .utils.geometry import get_clicked_position
from .models.a_star import a_star
# -------------------------------------------------------------------------------------------------------------------------------------------------

def main(window):
    """
    Apply:
    ------
    Metodo encargado de iniciar la aplicacion y gestionar los metodos necesarios para el funcionamiento de la misma.
    
    Parameters:
    -----------
    window: `pygame.display`
        Objeto de la clase de `pygame` mediante la cual se instancia la ventana mediante la aplicacion del metodo `set_mode`.
    
    Returns:
    --------
    - None.
    """
    # Instanciamos los valores inicialres para el inicio, fin y el parametro de control de ejecucion
    start, end, run = None, None, True

    # Ahora vamos a crear la cuadricula que contendra la red de cuadros
    grid = create_grid()

    # Ahora iniciamos la activacion de los procesos mediante un bucle
    while run:

        # Primero vamos a dibujar todas las cuadriculas de la red
        draw_network(window, grid)

        # Una vez dibujado necesitamos iterar sobre los eventes que se generen en la ventana
        for event in pygame.event.get():

            # El primer evento en controlar sera la salida del juego
            if event.type == pygame.QUIT:
                run = False

            # Ahora necesitamos verificar si se pulsa la tecla izquierda del raton
            if pygame.mouse.get_pressed()[0]:

                # Para este caso vamos a localizar la posicion donde se dio clic
                # Sobre dicha posicion localizaremos la cuadricula y marcaremos los 
                # puntos segun las caracteristicas de cada uno
                position = pygame.mouse.get_pos()
                row, column = get_clicked_position(position)
                point = grid[row][column]

                # Es importante señalar que siempre el primer clic sera tomado como punto 
                # de inicio, el segundo clic sera tomado como punto final y todos los demas 
                # clic seran las barreras entre el punto de inicio y el final

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
                row, column = get_clicked_position(position)
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

                # El primer evento en controlar sera el de ejecucion del 
                # algoritmo
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for point in row:
                            point.update_neighbors(grid)

                    # Una vez actualizamos todos los vecinos, llamamos al 
                    # algoritmo de la estrella
                    a_star(lambda: draw_network(window, grid), grid, start, end)

                # Y Ahora para controlar el reinicio usaremos la tacla `C`
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = create_grid()

    # Por ultimo cerramos la aplicacion
    pygame.quit()

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------