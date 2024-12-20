# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS / APIs NECESARIAS
# -------------------------------------------------------------------------------------------------------------------------------------------------
import pygame
from settings import GAP_GRID, ROWS, WHITE, RED, GREEN, BLACK, ORANGE, TURQUOISE, PURPLE
# -------------------------------------------------------------------------------------------------------------------------------------------------

class Point:
    """
    Descripcion
    -----------
    Clase para representar un punto en una red de cuadriculas.

    Esta clase es util en aplicaciones de visualizacion y algoritmos de navegacion que involucran graficos y nodos, como algoritmos de busqueda 
    de caminos.
    
    Notes:
    ------
    - Un `Point` es una abstraccion que permite manipular posiciones en la red de cuadriculas como si fueran nodos de un grafo, con metodos para 
    abrir, cerrar, bloquear, y definir puntos de inicio y fin.
    """

    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column
        self.width = GAP_GRID
        self.totalRows = ROWS
        self.color = WHITE
        self.x = row * GAP_GRID
        self.y = column * GAP_GRID
        self.neighbors = []

    def get_position(self) -> tuple[int, int]:
        """
        Descripcion
        -----------
        Devuelve la posicion del punto como una tupla (fila, columna).

        Retorna
        -------
        - Posicion del punto.
        """
        return self.row, self.column
    
    def is_closed(self) -> bool:
        """
        Verifica si el punto esta cerrado (no accesible).
        """
        return self.color == RED
    
    def is_open(self) -> bool:
        """
        Verifica si el punto esta abierto (accesible).
        """
        return self.color == GREEN
    
    def is_barrier(self) -> bool:
        """
        Verifica si el punto es una barrera (obstaculo).
        """
        return self.color == BLACK
    
    def is_start(self) -> bool:
        """
        Verifica si el punto es el punto de inicio.
        """
        return self.color == ORANGE
    
    def is_end(self) -> bool:
        """
        Verifica si el punto es el punto de destino.
        """
        return self.color == TURQUOISE
        
    def reset(self) -> None:
        """
        Restablece el punto a su estado inicial (blanco).
        """
        self.color = WHITE

    def mark_start(self) -> None:
        """
        Marca el punto como el inicio.
        """
        self.color = ORANGE

    def mark_closed(self) -> None:
        """
        Marca el punto como cerrado.
        """
        self.color = RED

    def mark_open(self) -> None:
        """
        Marca el punto como abierto.
        """
        self.color = GREEN
    
    def mark_barrier(self) -> None:
        """
        Marca el punto como una barrera.
        """
        self.color = BLACK

    def mark_end(self) -> None:
        """
        Marca el punto como el destino.
        """
        self.color = TURQUOISE

    def create_path(self) -> None:
        """
        Marca el punto como parte de la ruta.
        """
        self.color = PURPLE

    def drawing(self, window: pygame.Surface) -> None:
        """
        Descripcion
        -----------
        Dibuja el punto en una ventana de `pygame`.

        Parametros
        ----------
        window
            Ventana de `pygame` en la que se dibuja el punto.
        """
        # Aqui sencillamente dibujamos sobre la ventaja el punto segun las caracteristicas que posea dicho punto
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid: list) -> None:
        """
        Descripcion
        -----------
        Actualiza la lista de vecinos accesibles en funcion de la cuadricula.

        Parametros
        ----------
        grid
            Lista de listas anidadas que representa la cuadricula.
        """
        # Antes de comenzar con el calculo, necesitamos limpiar la lista de vecinos del punto
        self.neighbors = list()
        
        # Comprobacion del vecino inferior: verificamos si la fila actual no es la ultima 
        # y si el punto directamente debajo del punto actual no es barrera.
        # Si ambas condiciones son verdaderas se añade este punto a la lista de vecinos
        if self.row < self.totalRows-1 and not grid[self.row+1][self.column].is_barrier():
            self.neighbors.append(grid[self.row+1][self.column])

        # Comprobacion del vecino superior: verificamos si la fila actual no es la 
        # primera, y si el punto directamente arriba del punto actual no es una barrera.
        # En caso de ser ciertas ambas condiciones se añade a la lista de vecinos
        if self.row > 0 and not grid[self.row-1][self.column].is_barrier():
            self.neighbors.append(grid[self.row-1][self.column])
        
        # Comprobacion del vecino derecho: verificamos si la column actual no es la utlima columna 
        # y se comprueba si el punto directamente a la derecha del punto actual no es una barrera.
        # De ser afirmativa ambas condiciones se añade a la lista de vecinos
        if self.column < self.totalRows-1 and not grid[self.row][self.column+1].is_barrier():
            self.neighbors.append(grid[self.row][self.column+1])

        # Comprobacion del vecino izquierdo: verificamos si la columna actual no es 
        # primera y si elpunto directamente a la izquierda del actual no es una barrera.
        # En caso de ser afirmativas ambas condiciones, agregamos el punto a la lista de vecinos
        if self.column > 0 and not grid[self.row][self.column-1].is_barrier():
            self.neighbors.append(grid[self.row][self.column-1])

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------