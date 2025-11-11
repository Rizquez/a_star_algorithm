# MODULES (EXTERNAL)
# ---------------------------------------------------------------------------------------------------------------------
import pygame
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from pygame import Surface
# ---------------------------------------------------------------------------------------------------------------------

# MODULES (INTERNAL)
# ---------------------------------------------------------------------------------------------------------------------
from src.core import *
from src.models import *
from settings import ROWS, WHITE, WINDOW_WIDTH, GAP_GRID, GREY
# ---------------------------------------------------------------------------------------------------------------------

# OPERATIONS / CLASS CREATION / GENERAL FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------------

def main_method(window: 'Surface') -> None:
    """
    Starts the application and manages events for the program's operation.

    This main method controls the user interaction logic, such as drawing the grid network, 
    setting start and end points, marking barriers, and executing the A* algorithm. It also 
    allows the network to be restarted.
    
    Args:
        window (Surface):
            `pygame` window in which the point is drawn.
    """
    # We instantiate the initial values for the start, end, and execution control parameter
    start, end, run = None, None, True

    # Now we are going to create the grid that will contain the network of squares
    grid = _create_grid()

    # Now we start activating the processes using a loop
    while run:

        # First, let's draw all the grid squares
        _draw_network(window, grid)

        # Once drawn, we need to iterate over the events generated in the window
        for event in pygame.event.get():

            # The first event to monitor will be the game's release
            if event.type == pygame.QUIT:
                run = False

            # Now we need to check if the left mouse button is pressed
            if pygame.mouse.get_pressed()[0]:

                # In this case, we will locate the position where the click occurred
                # At that position, we will locate the grid and mark the points according 
                # to the characteristics of each one
                position = pygame.mouse.get_pos()
                row, column = _get_clicked_position(position)
                point = grid[row][column]

                # It is important to note that the first click will always be 
                # taken as the starting point, the second click will be taken 
                # as the end point, and all other clicks will be the barriers 
                # between the starting point and the end point

                # If the starting point is not marked
                if not start and point != end:
                    start = point
                    start.mark_start()

                # If the end point is not marked
                elif not end and point != start:
                    end = point
                    end.mark_end()

                # About the points of the barriers
                else:
                    point.mark_barrier()

            # Now let's check if the right mouse button is being clicked
            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, column = _get_clicked_position(position)
                point = grid[row][column]
                point.reset()

                # Resetting the values of the starting point
                if point == start:
                    start = None

                # Resetting endpoint values
                elif point == end:
                    end = None

                else:
                    pass

            # Now the idea would be to evaluate the event that starts 
            # the execution of the algorithm and restarts the grid network
            # To handle these events, we will focus on the keys
            if event.type == pygame.KEYDOWN:

                # The first event to be controlled will be the execution of the algorithm
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for point in row:
                            point.update_neighbors(grid)

                    # Once we update all the neighbors, we call the star algorithm
                    a_star(lambda: _draw_network(window, grid), grid, start, end)

                # And now to control the restart we will use the C key.
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = _create_grid()

    # Finally, we close the application
    pygame.quit()

def _get_clicked_position(position: Tuple) -> Tuple[int, int]:
    """
    Obtains the row and column where a click occurs on the grid.

    Args:
        position (Tuple):
            Coordinates `(x, y)` of the user's click.

    Returns:
        Tuple:
            Row and column where the click occurred.
    """
    # We extract the coordinates
    y, x = position

    # Now we need to calculate the row and column based on the coordinates
    row = y // GAP_GRID
    column = x // GAP_GRID
    
    return row, column

def _create_grid() -> List:
    """
    Creates the grid network used in the program.

    This function generates a two-dimensional list representing the rows and columns of the grid.

    Returns:
        List:
            List of nested lists with `Point` objects representing each cell in the grid.
    
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

def _draw_network(window: 'Surface', grid: List) -> None:
    """
    Draw the grid in the window.

    Args:
        window (Surface):
            `pygame` window in which the point is drawn.
        grid (List):
            List of nested lists representing the grid network.
    """
    # First, we define the color of the window. 
    window.fill(WHITE)
    
    # Now we are going to iterate over the list with the grid network data
    # And for each sublist, we are going to capture the point that has been created 
    # to draw it, applying the internal method of the class that manages the points
    for row in grid:
        for point in row:
            point.drawing(window)

    # Once each point has been drawn, we will outline the contours to separate them visually
    # When finished, we will need to update the window
    _draw_squares(window)
    pygame.display.update()

def _draw_squares(window: 'Surface') -> None:
    """
    Draw the grid lines in the window.

    Args:
        window (Surface):
            `pygame` window in which the point is drawn.
    """
    # Constant to indicate the starting coordinate of the line
    START_POINT = 0

    # Now we're just going to iterate over the number of rows to outline the edges of each grid
    for row in range(ROWS):
        pygame.draw.line(window, GREY, (START_POINT, row * GAP_GRID), (WINDOW_WIDTH, row * GAP_GRID))
        for column in range(ROWS):
            pygame.draw.line(window, GREY, (column * GAP_GRID, START_POINT), (column * GAP_GRID, WINDOW_WIDTH))

# ---------------------------------------------------------------------------------------------------------------------
# END OF FILE