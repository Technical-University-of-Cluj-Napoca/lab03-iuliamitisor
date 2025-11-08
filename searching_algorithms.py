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
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor) # visit the neighbors
                came_from[neighbor] = current # and add them to path
                queue.append(neighbor) # enqueue to visit later on
                neighbor.make_open()
    
        draw()
        if current != start:
            current.make_closed()
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
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor) # visit the neighbors
                came_from[neighbor] = current # and add them to path
                stack.append(neighbor) # push to visit later on
                neighbor.make_open()
    
        draw()
        if current != start:
            current.make_closed()
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

def astar(draw: callable, grid: Grid, start: Spot, end: Spot, heuristic="Manhattan") -> bool:
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
    f_score[start] = heuristic(start.get_position(), end.get_position())
    open_set = {start}

    while not open_heap.empty():
        current = open_heap.get()[2]
        open_set.remove(current)

        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            tentative_g = g_score[current] + 1
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor.get_position(), end.get_position())
                if neighbor not in open_set:
                    count += 1
                    open_heap.put((f_score[neighbor], count, neighbor))
                    open_set.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()

    return False

def dls(draw: callable, grid: Grid, start: Spot, end: Spot, limit: int) -> bool:
    """
    Depth-Limited Search (DLS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
        limit (int): The depth limit for the search.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    def dls_util(current: Spot, depth: int) -> bool:
        # mark current as visited
        visited.add(current)
        if current != start:
            current.make_open()
        draw()

        if current == end:
            return True
        if depth <= 0:
            # depth limit reached
            if current != start:
                current.make_closed()
                draw()
            return False
        
        for neighbor in current.neighbors:
            if neighbor in visited:
                continue
            if dls_util(neighbor, depth - 1):
                came_from[neighbor] = current
                return True

        # finished exploring this branch, mark closed
        if current != start:
            current.make_closed()
            draw()
        return False
    

    if start is None or end is None:
        return False
    came_from = {}
    visited = set()
    if dls_util(start, limit):
        current = end
        while current in came_from:
            current = came_from[current]
            current.make_path()
            draw()
        end.make_end()
        start.make_start()
        return True
    return False

def ucs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Uninformed Cost Search (UCS) Algorithm.
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
    count = 0
    open_heap = PriorityQueue()
    open_heap.put((0, count, start))
    came_from = {}
    cost_so_far = {start: 0}

    while not open_heap.empty():
        current_cost, _, current = open_heap.get()

        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            new_cost = cost_so_far[current] + 1 # each step has a cost of 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost
                count += 1
                open_heap.put((priority, count, neighbor))
                came_from[neighbor] = current
                neighbor.make_open()
    
        draw()
        if current != start:
            current.make_closed()
    return False

def greedy(draw: callable, grid: Grid, start: Spot, end: Spot, heuristic="Manhattan") -> bool:
    """
    Greedy Search Algorithm.
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
    open_heap = PriorityQueue()
    open_heap.put((0, start))
    came_from = {}
    visited = {start}

    while not open_heap.empty():
        current = open_heap.get()[1]

        if current == end:
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                priority = heuristic(neighbor.get_position(), end.get_position())
                open_heap.put((priority, neighbor))
                came_from[neighbor] = current
                neighbor.make_open()
    
        draw()
        if current != start:
            current.make_closed()
    return False

def iddfs(draw: callable, grid: Grid, start: Spot, end: Spot, max_depth: int) -> bool:
    """
    Iterative Deepening Depth-First Search (IDDFS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
        max_depth (int): The maximum depth limit for the search.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    for depth in range(max_depth + 1):
        if dls(draw, grid, start, end, depth):
            return True
    return False

def ida(draw: callable, grid: Grid, start: Spot, end: Spot, heuristic="Manhattan") -> bool:
    """
    Iterative Deepening A* (IDA*) Algorithm adapted for grid visualization.
    Args:
        draw (callable): Function to update the display.
        grid (Grid): The Grid object.
        start (Spot): Start node.
        end (Spot): End node.
    Returns:
        bool: True if path found, else False.
    """
    def search(path: list[Spot], g: float, threshold: float, came_from: dict) -> float | list[Spot]:
        """
        Recursive depth-limited A* search.
        Returns either:
        - a float (new threshold if path not found within limit), or
        - a list of Spots (the successful path)
        """
        current = path[-1] # last node
        f = g + heuristic(current.get_position(), end.get_position())
        if f > threshold:
            return f
        if current == end:
            return path
        min_threshold = float("inf")

        # mark as open
        if current != start and current != end:
            current.make_open()
            draw()

        for neighbor in current.neighbors:
            if neighbor in path:
                continue # no cycles allowed
            path.append(neighbor)
            came_from[neighbor] = current
            res = search(path, g + 1, threshold, came_from)
            if isinstance(res, list): # found a valid path
                return res
            if res < min_threshold:
                min_threshold = res
            path.pop()
            if neighbor != start and neighbor != end:
                neighbor.make_closed()
                draw()

        return min_threshold

    threshold = heuristic(start.get_position(), end.get_position())
    came_from = {}
    path = [start]
    while True:
        res = search(path, 0, threshold, came_from)
        if isinstance(res, list):
            # reconstruct path
            for spot in res:
                if spot != start and spot != end:
                    spot.make_path()
                    draw()
            end.make_end()
            start.make_start()
            return True
        if res == float("inf"):
            return False
        threshold = res  # increase the depth threshold