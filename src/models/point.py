# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS / APIs NECESARIAS
# -------------------------------------------------------------------------------------------------------------------------------------------------
import pygame
from ..config.config import GAP_GRID, ROWS, WHITE, RED, GREEN, BLACK, ORANGE, TURQUOISE, PURPLE
# -------------------------------------------------------------------------------------------------------------------------------------------------

class Point:
    """
    Apply:
    ------
    Clase diseñada para representa un punto en una red de cuadriculas, utilizada en este caso sobre aplicaciones de visualizacion y algoritmos 
    que involucran graficos y navegacion por nodos, como algoritmos de busqueda de caminos.
    
    Notes:
    ------
    - Un `Point` es una abstraccion que permite manipular posiciones en la red de cuadriculas como si fueran nodos de un grafo, con metodos para 
    abrir, cerrar, bloquear, y definir puntos de inicio y fin.
    - La informacion detallada acerca del alcance de aplicacion de cada método público se encuentra internamente en su respectiva documentacion.

    Parameters:
    -----------
    row: `int`
        La fila en la red de cuadriculas donde se encuentra el punto.

    column: `int`
        La columna en la red de cuadriculas donde se encuentra el punto.

    Attributes:
    -----------
    - Fila del punto en la red de cuadriculas.
    - Columna del punto en la red de cuadriculas.
    - Ancho de la celda que ocupa el punto en la red de cuadriculas.
    - Numero total de filas en la red de cuadriculas.
    - Color actual del punto (Se usa constantes de color para indicar diferentes estados).
    - Posicion `x` del punto en la ventana de visualizacion.
    - Posicion `y` del punto en la ventana de visualizacion.
    - Lista de puntos vecinos que no son barreras.

    Public Methods:
    ---------------
    - `get_position()`
    - `closed()`
    - `opened()`
    - `barrier()`
    - `start()`
    - `end()`
    - `reset()`
    - `do_start()`
    - `do_closed()`
    - `do_opened()`
    - `do_barrier()`
    - `do_end()`
    - `do_path`
    - `drawing()`
    - `update_neighbors()`
    """
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    # ******** METODO CONSTRUCTOR DE LA CLASE ********

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.width = GAP_GRID
        self.totalRows = ROWS
        self.color = WHITE
        self.x = row * GAP_GRID
        self.y = column * GAP_GRID
        self.neighbors = []

    # ---------------------------------------------------------------------------------------------------------------------------------------------
    # ******** METODOS GENERALES DE LA CLASE ********

    def get_position(self):
        """
        Apply:
        ------
        Metodo diseñado para devolver la posicion del punto como una tupla (fila, columna).

        Parameters:
        -----------
        - None.

        Returns:
        --------
        - Posicion del punto en la fila.
        - Posicion del punto en la columna.
        """
        return self.row, self.column
    
    def is_closed(self):
        """
        Apply:
        ------
        Metodo para verificar si el punto esta cerrado (no accesible).

        Parameters:
        -----------
        - None.

        Returns:
        --------
        - `True` | `False`
        """
        return self.color == RED
    
    def is_open(self):
        """
        Apply:
        ------
        Metodo para verificar si el punto esta abierto (accesible).

        Parameters:
        -----------
        - None.

        Returns:
        --------
        - `True` | `False`
        """
        return self.color == GREEN
    
    def is_barrier(self):
        """
        Apply:
        ------
        Metodo para verificar si el punto es una barrera (obstaculo).

        Parameters:
        -----------
        - None.

        Returns:
        --------
        - `True` | `False`
        """
        return self.color == BLACK
    
    def is_start(self):
        """
        Apply:
        ------
        Metodo para verificar si el punto es el punto de inicio en la red de cuadriculas.

        Parameters:
        -----------
        - None.

        Returns:
        --------
        - `True` | `False`
        """
        return self.color == ORANGE
    
    def is_end(self):
        """
        Apply:
        ------
        Metodo para verificar si el punto es el punto de destino en la red de cuadriculas.

        Parameters:
        -----------
        - None.

        Returns:
        --------
        - `True` | `False`
        """
        return self.color == TURQUOISE
        
    def reset(self):
        """
        Apply:
        ------
        Medoto para restablecer el punto a su estado inicial (blanco).

        Parameters:
        -----------
        - None.

        Returns:
        --------
        - None
        """
        self.color = WHITE

    def mark_start(self):
        """
        Apply:
        ------
        Metodo para marcar el punto como el inicio.

        Parameters:
        -----------
        - None.

        Returns:
        --------
        - None
        """
        self.color = ORANGE

    def mark_closed(self):
        """
        Apply:
        ------
        Metodo para marcar el punto como cerrado.

        Parameters:
        -----------
        - None.

        Returns:
        --------
        - None
        """
        self.color = RED

    def mark_open(self):
        """
        Apply:
        ------
        Metodo para marcar el punto como abierto.

        Parameters:
        -----------
        - None.

        Returns:
        --------
        - None
        """
        self.color = GREEN
    
    def mark_barrier(self):
        """
        Apply:
        ------
        Metodo para marcar el punto como una barrera.

        Parameters:
        -----------
        - None.

        Returns:
        --------
        - None
        """
        self.color = BLACK

    def mark_end(self):
        """
        Apply:
        ------
        Metodo para marcar el punto como el destino.

        Parameters:
        -----------
        - None.

        Returns:
        --------
        - None
        """
        self.color = TURQUOISE

    def create_path(self):
        """
        Apply:
        ------
        Metodo para crear la ruta de conexion entre el punto inicio y el punto fin.

        Parameters:
        -----------
        - None.

        Returns:
        --------
        - None
        """
        self.color = PURPLE

    def drawing(self, window):
        """
        Apply:
        ------
        Metodo encargado de dibujar el punto sobre la ventaja mediante la posicion que posea.

        Parameters:
        -----------
        window: `pygame.display`
            Objeto de la clase de `pygame` mediante la cual se instancia la ventana mediante la aplicacion del metodo `set_mode`.

        Returns:
        --------
        - None.
        """
        # Aqui sencillamente dibujamos sobre la ventaja el punto segun las caracteristicas que posea dicho punto
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        """
        Apply:
        ------
        Metodo encargado de actualizar la lista de vecinos accesibles basandose en la red de cuadriculas enviada por el parametro `grid`.

        Parameters:
        -----------
        grid: `list`
            Lista de listas anidadas con las dimensiones de la red de cuadriculas.

        Returns:
        --------
        - None.
        """
        # Antes de comenzar con el calculo, necesitamos limpiar la lista de vecinos del punto
        self.neighbors = list()
        
        # Comprobacion del vecino inferior: verificamos si la fila actual no es la ultima y si
        # el punto directamente debajo del punto actual no es barrera.
        # Si ambas condiciones son verdaderas se añade este punto a la lista de vecinos
        if self.row < self.totalRows-1 and not grid[self.row+1][self.column].is_barrier():
            self.neighbors.append(grid[self.row+1][self.column])

        # Comprobacion del vecino superior: verificamos si la fila actual no es la primera, y si 
        # el punto directamente arriba del punto actual no es una barrera.
        # En caso de ser ciertas ambas condiciones se añade a la lista de vecinos
        if self.row > 0 and not grid[self.row-1][self.column].is_barrier():
            self.neighbors.append(grid[self.row-1][self.column])
        
        # Comprobacion del vecino derecho: verificamos si la column actual no es la utlima columna
        # y se comprueba si el punto directamente a la derecha del punto actual no es una barrera.
        # De ser afirmativa ambas condiciones se añade a la lista de vecinos
        if self.column < self.totalRows-1 and not grid[self.row][self.column+1].is_barrier():
            self.neighbors.append(grid[self.row][self.column+1])

        # Comprobacion del vecino izquierdo: verificamos si la columna actual no es primera y si el
        # punto directamente a la izquierda del actual no es una barrera.
        # En caso de ser afirmativas ambas condiciones, agregamos el punto a la lista de vecinos
        if self.column > 0 and not grid[self.row][self.column-1].is_barrier():
            self.neighbors.append(grid[self.row][self.column-1])

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------