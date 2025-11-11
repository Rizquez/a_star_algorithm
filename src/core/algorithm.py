# MODULES (EXTERNAL)
# ---------------------------------------------------------------------------------------------------------------------
from queue import PriorityQueue
from typing import Callable, List, Tuple, Dict, TYPE_CHECKING
# ---------------------------------------------------------------------------------------------------------------------

# MODULES (INTERNAL)
# ---------------------------------------------------------------------------------------------------------------------
if TYPE_CHECKING:
    from src.models import Point
# ---------------------------------------------------------------------------------------------------------------------

# OPERATIONS / CLASS CREATION / GENERAL FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------------

def a_star(draw: Callable, grid: List, start: 'Point', end: 'Point') -> bool:
    """
    Implementation of the A* pathfinding algorithm.

    This method finds the shortest path in a network of nodes from a starting node (`start`) to an ending node (`end`). 

    It uses a priority queue to select the most promising nodes based on a heuristic.
    
    Args:
        draw (Callable):
            Function to draw the current state of the grid.
        grid (List):
            List of nested lists representing the grid network.
        start (Point):
            Start node.

        end (Point):
            Destination node.

    Returns:
        bool:
            `True` if a path is found from the start node to the end node, or `False` if no path is found.
    """
    # First, let's instantiate a counter to maintain the insertion order in the priority queue
    count = 0

    # We will instantiate an object of the `PriorityQueue` class to store the nodes to be explored, 
    # sorted by their `f_score`
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    # The `came_from` dictionary will help us trace the path traveled.
    came_from = {}

    # On the other hand, from the A* algorithm theory, we know that `g_score` is a dictionary that will 
    # store the cost of the shortest path from the initial node to each node to be studied, while `f_score` 
    # is a dictionary that will store the estimated total cost from the initial node to the final node, passing 
    # through each node
    g_score = {point: float("inf") for row in grid for point in row}
    g_score[start] = 0
    f_score = {point: float("inf") for row in grid for point in row}
    f_score[start] = _distance_between_points(start.get_position(), end.get_position())

    # This dictionary will help us quickly track whether a node is in `open_set`
    open_set_hash = {start}

    # Now if we start the loop while values exist
    while not open_set.empty():

        # We capture the current node and remove it from the hash table
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # The first thing we are going to check is whether the current node is the final node
        # If this is true, we will construct the path and return True
        if current == end:
            _reconstruct_path(came_from, end, draw)
            end.mark_end()
            return True

        # Meanwhile, if the above condition is not met, we must iterate over the 
        # neighbors of the current node
        for neighbor in current.neighbors:

            # For each neighbor of the node, a temporary `g_score` will be calculated to compare it with 
            # the existing `g_score`. If this `temp_g_score` is lower than the `g_score`, we will update 
            # the neighbor's `came_from`, `g_score`, and `f_score` dictionaries
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = g_score[neighbor] + _distance_between_points(neighbor.get_position(), end.get_position())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.mark_open()

        # Now we must update the visualization of the nodes
        draw()
        
        # If the current node is different from the start node, we mark it as closed
        if current != start:
            current.mark_closed()

    return False

def _reconstruct_path(came_from: Dict, current: 'Point', draw: Callable) -> None:
    """
    Reconstructs the path from the initial node to the final node.
    
    Args:
        came_from (Dict):
            Dictionary that assigns each node to the node from which it originates.
        current (Point):
            Current node being examined.
        draw (Callable):
            Function to draw the current state of the grid.
    """
    # We start a loop on the node dictionary
    # For each iteration, the node is updated, and we call the `create_path` method to mark the node as part of the path
    # The last method to be called is draw, which is responsible for displaying the node's status
    while current in came_from:
        current = came_from[current]
        current.create_path()
        draw()

def _distance_between_points(point1: Tuple, point2: Tuple) -> int:
    """
    Calculates the distance between two points in a network of nodes.

    This method uses the Manhattan distance to calculate the distance between two nodes.

    Args
        point1 (Tuple):
            Coordinates `(x, y)` of the first point.
        point2 (Tuple):
            Coordinates `(x, y)` of the second point.

    Returns:
        int:
            Calculated distance between the points.
    """
    # First, we extract the coordinates of the points and then calculate and return the value
    x1, y1 = point1
    x2, y2 = point2

    return abs(x1-x2) + abs(y1-y2)

# ---------------------------------------------------------------------------------------------------------------------
# END OF FILE