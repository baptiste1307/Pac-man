from collections import deque


def _get_neighbors(maze, x, y):
    rows = len(maze)
    cols = len(maze[0])
    cell = maze[y][x]

    if not (cell & 1) and y > 0:
        yield (x, y - 1)
    if not (cell & 2) and x < cols - 1:
        yield (x + 1, y)
    if not (cell & 4) and y < rows - 1:
        yield (x, y + 1)
    if not (cell & 8) and x > 0:
        yield (x - 1, y)


def find_shortest_path(maze, start, goal):
    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        for neighbor in _get_neighbors(maze, *current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    if goal not in came_from:
        return []

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = came_from[current]

    path.reverse()
    return path
