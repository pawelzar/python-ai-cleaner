from src.priority_queue import *


def heuristic(a, b):
    """Return absolute distance from point a to b."""
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph, start, goal):
    """Return list of points and list of costs created by A* algorithm."""
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far


def reconstruct_path(came_from, start, goal):
    """Return list of points that represents the path created by A* algorithm."""
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def path_as_states(path):
    """Return list of move directions for the agent."""
    states = []
    (x_prev, y_prev) = path[0]

    for x, y in path[1:]:
        if y - y_prev < 0:
            states.append('up')
        elif y - y_prev > 0:
            states.append('down')
        elif x - x_prev < 0:
            states.append('left')
        elif x - x_prev > 0:
            states.append('right')
        (x_prev, y_prev) = (x, y)

    return states
