# MODULES (EXTERNAL)
# ---------------------------------------------------------------------------------------------------------------------
import pygame
from typing import Tuple, List, TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Surface
# ---------------------------------------------------------------------------------------------------------------------

# MODULES (INTERNAL)
# ---------------------------------------------------------------------------------------------------------------------
from settings import *
# ---------------------------------------------------------------------------------------------------------------------

# OPERATIONS / CLASS CREATION / GENERAL FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------------

class Point:
    """
    Class for representing a point in a grid network.

    This class is useful in visualization applications and navigation algorithms involving graphs and nodes, 
    such as pathfinding algorithms.
    
    Notes:
        - A `Point` is an abstraction that allows you to manipulate positions in the grid network as if they were 
        nodes in a graph, with methods for opening, closing, locking, and defining start and end points.
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

    def get_position(self) -> Tuple[int, int]:
        """
        Returns the position of the point as a tuple (row, column).

        Returns:
            Tuple:
                Position of the point.
        """
        return self.row, self.column
    
    def is_closed(self) -> bool:
        """
        Check if the point is closed (not accessible).
        """
        return self.color == RED
    
    def is_open(self) -> bool:
        """
        Check if the point is open (accessible).
        """
        return self.color == GREEN
    
    def is_barrier(self) -> bool:
        """
        Check if the point is a barrier (obstacle).
        """
        return self.color == BLACK
    
    def is_start(self) -> bool:
        """
        Check if the point is the starting point.
        """
        return self.color == ORANGE
    
    def is_end(self) -> bool:
        """
        Verify that the point is the destination point.
        """
        return self.color == TURQUOISE
        
    def reset(self) -> None:
        """
        Resets the point to its initial state (white).
        """
        self.color = WHITE

    def mark_start(self) -> None:
        """
        Mark the point as the start.
        """
        self.color = ORANGE

    def mark_closed(self) -> None:
        """
        Mark the point as closed.
        """
        self.color = RED

    def mark_open(self) -> None:
        """
        Mark the point as open.
        """
        self.color = GREEN
    
    def mark_barrier(self) -> None:
        """
        Mark the point as a barrier.
        """
        self.color = BLACK

    def mark_end(self) -> None:
        """
        Mark the point as the destination.
        """
        self.color = TURQUOISE

    def create_path(self) -> None:
        """
        Mark the point as part of the route.
        """
        self.color = PURPLE

    def drawing(self, window: 'Surface') -> None:
        """
        Draw the point in a `pygame` window.

        Here, simply draw the point on the edge according 
        to the characteristics of that point.
        
        Args:
            window (Surface):
                `pygame` window in which the point is drawn.
        """
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid: List) -> None:
        """
        Update the list of accessible neighbors based on the grid.

        Args:
            grid (List):
                List of nested lists representing the grid.
        """
        # Before starting the calculation, we need to clear the list of neighbors of the point
        self.neighbors = list()
        
        # Checking the lower neighbor: we verify that the current row is not the last 
        # one and that the point directly below the current point is not a barrier
        # If both conditions are true, this point is added to the list of neighbors
        if self.row < self.totalRows-1 and not grid[self.row+1][self.column].is_barrier():
            self.neighbors.append(grid[self.row+1][self.column])

        # Checking the upper neighbor: we verify that the current row is not the first 
        # one, and that the point directly above the current point is not a barrier
        # If both conditions are true, it is added to the list of neighbors
        if self.row > 0 and not grid[self.row-1][self.column].is_barrier():
            self.neighbors.append(grid[self.row-1][self.column])
        
        # Checking the right neighbor: we verify that the current column is not the last column 
        # and check that the point directly to the right of the current point is not a barrier
        # If both conditions are true, it is added to the list of neighbors
        if self.column < self.totalRows-1 and not grid[self.row][self.column+1].is_barrier():
            self.neighbors.append(grid[self.row][self.column+1])

        # Checking the left neighbor: we verify that the current column is not the first 
        # one and that the point directly to the left of the current one is not a barrier
        # If both conditions are true, we add the point to the list of neighbors
        if self.column > 0 and not grid[self.row][self.column-1].is_barrier():
            self.neighbors.append(grid[self.row][self.column-1])

# ---------------------------------------------------------------------------------------------------------------------
# END OF FILE