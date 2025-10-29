from utils import *
from collections import deque
from queue import PriorityQueue
from grid import Grid
from spot import Spot

def bfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Breadth-First Search (BFS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    if start is None or end is None:
        return False    
    queue = deque()
    queue.append(start)
    visited = {start}
    came_from = {}

    while queue:
        current = queue.popleft()
        if current == end: # if destination found reconstruct path
            while current in came_from:
                current = came_from[current]
                current.make_path() # color purple
                draw()
            end.make_end() # color yellow
            start.make_start() # color orange
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor) # visit the neighbors
                came_from[neighbor] = current # and add them to path
                queue.append(neighbor) # enqueue to visit later on
                neighbor.make_open() # color green
    
        draw()
        if current != start:
            current.make_closed() # color red
    return False

def dfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Depth-First Search (DFS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    if start is None or end is None:
        return False    
    stack = [start]
    visited = {start}
    came_from = {}

    while stack:
        current = stack.pop()
        if current == end: # if destination found reconstruct path
            while current in came_from:
                current = came_from[current]
                current.make_path() # color purple
                draw()
            end.make_end() # color yellow
            start.make_start() # color orange
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor) # visit the neighbors
                came_from[neighbor] = current # and add them to path
                stack.append(neighbor) # push to visit later on
                neighbor.make_open() # color green
    
        draw()
        if current != start:
            current.make_closed() # color red
    return False

def h_manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Manhattan distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Manhattan distance between p1 and p2.
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def h_euclidian_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Euclidian distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Euclidean distance between p1 and p2.
    """
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def astar(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    A* Pathfinding Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    count = 0
    open_heap = PriorityQueue()
    open_heap.put((0, count, start))

    came_from = {}
    g_score = {}
    f_score = {}

    for row in grid.grid:
        for spot in row:
            g_score[spot] = float("inf")
            f_score[spot] = float("inf")

    g_score[start] = 0 
    
    print(start.get_position())
    f_score[start] = h_manhattan_distance(start.get_position(), end.get_position())
    open_set = {start}

    while not open_heap.empty():
        current = open_heap.get()[2]
        open_set.remove(current)

        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path() # color purple
                draw()
            end.make_end() # color yellow
            start.make_start() # color orange
            return True
        
        for neighbor in current.neighbors:
            tentative_g = g_score[current] + 1
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + h_manhattan_distance(neighbor.get_position(), end.get_position())
                if neighbor not in open_set:
                    count += 1
                    open_heap.put((f_score[neighbor], count, neighbor))
                    open_set.add(neighbor)
                    neighbor.make_open() # color green
        draw()
        if current != start:
            current.make_closed() # color red

    return False

# and the others algorithms...
# ▢ Depth-Limited Search (DLS)
# ▢ Uninformed Cost Search (UCS)
# ▢ Greedy Search
# ▢ Iterative Deepening Search/Iterative Deepening Depth-First Search (IDS/IDDFS)
# ▢ Iterative Deepening A* (IDA)
# Assume that each edge (graph weight) equalss