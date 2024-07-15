# -------------------------------------------------------------------------------------------------------------------------------------------------
# LIBRERIAS / APIs NECESARIAS
# -------------------------------------------------------------------------------------------------------------------------------------------------
from queue import PriorityQueue
from ..utils.geometry import distance_between_points
# -------------------------------------------------------------------------------------------------------------------------------------------------

def _reconstruct_path(came_from, current, draw):
    """
    Apply:
    ------
    Metodo encargado de reconstruir la ruta desde el nodo inicial hasta el nodo final.
    
    Parameters:
    -----------
    came_from: `dict`
        Diccionario que asigna cada nodo al nodo del que procede.
    
    current: `node`
        Nodo actual que se está examinando.
    
    draw: `function`
        Funcion para dibujar el estado actual de la cuadricula.

    Returns:
    --------
    - None.
    """
    # Iniciamos un bucle sobre el diccionario de nodos
    # Por cada iteracion se actualiza el nodo y llamamos al metodo 
    # `create_path` para marcar el nodo como parte del camino.
    # El ultimo metodo en ser llamado es draw, el cual se encarga 
    # de visualizar el estado del nodo.
    while current in came_from:
        current = came_from[current]
        current.create_path()
        draw()


def a_star(draw, grid, start, end):
    """
    Apply:
    ------
    Metodo de implementacion del algoritmo de Pathfinding A*.
    
    Parameters:
    -----------
    draw: `function`
        Funcion para dibujar el estado actual de la cuadricula.
    
    grid: `list`
        Lista de listas anidadas con las dimensiones de la red de cuadriculas.
    
    start: `node`
        Nodo de inicio.
    
    end: `node`
        Nodo de fin.

    Returns:
    --------
    - True si se encuentra una ruta, False en caso contrario.
    """
    # Primero vamos a instanciar un contador para mantener el orden de insercion en la 
    # cola de prioridad.
    count = 0

    # Entonces instanciaremos un objeto de la clase `PriorityQueue` para guardar los nodos 
    # por explorar, ordenados por su `f_score`
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    # El diccionario `came_from` nos ayudara a rastrear el camino recorrido
    came_from = {}

    # Por otro lado, desde la teoria del algoritmo A* sabemos que, `g_score` es un diccionario que
    # almacenara el coste del desplazamiento mas corto desde el nodo inicial a cada nodo a estudiar
    # mientas que `f_score` es un diccionario que almacenara la estimacion del costo total del nodo 
    # inicial al nodo final, pasando por cada nodo
    g_score = {point: float("inf") for row in grid for point in row}
    g_score[start] = 0
    f_score = {point: float("inf") for row in grid for point in row}
    f_score[start] = distance_between_points(start.get_position(), end.get_position())

    # Este diccionario nos ayudara a rastrear rapidamente si un nodo esta en `open_set`
    open_set_hash = {start}

    # Ahora si arrancamos el bucle mientras existan valores
    while not open_set.empty():

        # Capturamos el nodo actual y lo eliminamos del registro hash
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # Lo primero que vamos a verificar es si el nodo actual es el nodo final
        # En caso de ser cierto, vamos a construir la ruta y retornamos el True
        if current == end:
            _reconstruct_path(came_from, end, draw)
            end.mark_end()
            return True

        # Mientras tanto, si la condicion de arriba no se cumple debemos iterar sobre los 
        # nodos vecinos del nodo actual
        for neighbor in current.neighbors:

            # Para cada vecino del nodo se calculara un `g_score` temporal para compararlo con el 
            # `g_score` que existe, si este `temp_g_score` es menor que el `g_score`, actualizaremos 
            # los diccionarios `came_from`, `g_score` y `f_score` del vecino.
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = g_score[neighbor] + distance_between_points(neighbor.get_position(), end.get_position())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.mark_open()

        # Ahora debemos ir actualizano la vizualizacion de los nodos.
        draw()
        
        # Si el nodo actual es distinto del nodo de inicio lo marcamos como cerrado
        if current != start:
            current.mark_closed()

    return False

# -------------------------------------------------------------------------------------------------------------------------------------------------
# FIN DEL FICHERO
# -------------------------------------------------------------------------------------------------------------------------------------------------