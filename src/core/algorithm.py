import math

from model.pqueue import PriorityQueue


def heuristic(a, b):
    """
    Return absolute distance from point a to b.
    Strictly horizontal and/or vertical path.
    """
    (x_1, y_1) = a
    (x_2, y_2) = b
    return abs(x_1 - x_2) + abs(y_1 - y_2)


def euclidean(a, b):
    """
    Return Euclidean distance from point a to point b.
    """
    (x_1, y_1) = a
    (x_2, y_2) = b
    return math.sqrt((x_1 - x_2) ** 2 + (y_1 - y_2) ** 2)


def count_cost(start, goal, state):
    """
    Return cost of agent move, including rotations.
    """
    (x, y) = start
    (x_next, y_next) = goal
    new_state = state
    cost = 0

    if state == 'up':  # 0 degrees (UP)
        if y_next < y:
            pass
        elif y_next > y:
            new_state = 'down'
            cost = 2
        elif x_next < x:
            new_state = 'left'
            cost = -1
        elif x_next > x:
            new_state = 'right'
            cost = 1
    elif state == 'right':  # 90 degrees (RIGHT)
        if y_next < y:
            new_state = 'up'
            cost = -1
        elif y_next > y:
            new_state = 'down'
            cost = 1
        elif x_next < x:
            new_state = 'left'
            cost = 2
        elif x_next > x:
            pass
    elif state == 'down':  # 180 degrees (DOWN)
        if y_next < y:
            new_state = 'up'
            cost = 2
        elif y_next > y:
            pass
        elif x_next < x:
            new_state = 'left'
            cost = 1
        elif x_next > x:
            new_state = 'right'
            cost = -1
    elif state == 'left':  # 270 degrees (LEFT)
        if y_next < y:
            new_state = 'up'
            cost = 1
        elif y_next > y:
            new_state = 'down'
            cost = -1
        elif x_next < x:
            pass
        elif x_next > x:
            new_state = 'right'
            cost = 2

    return new_state, cost


def a_star_search(graph, start, goal, state='up'):
    """
    Return list of points, which is the path created by A* algorithm.
    """
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty:
        current = frontier.get()

        if current == goal:
            break

        for position in graph.neighbors(current):
            state, rotate_cost = count_cost(current, position, state)
            new_cost = (
                cost_so_far[current] +
                graph.cost(current, position) +
                abs(rotate_cost)
            )
            if position not in cost_so_far or new_cost < cost_so_far[position]:
                cost_so_far[position] = new_cost
                priority = new_cost + heuristic(goal, position)
                frontier.put(position, priority)
                came_from[position] = current

    return reconstruct_path(came_from, start, goal)


def reconstruct_path(came_from, start, goal):
    """
    Return list of points that represents the path created by A* algorithm.
    """
    current = goal
    path = [current]

    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()

    return path


def path_as_states(path):
    """
    Return list of move directions for the agent.
    """
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


def path_as_orders(path, rotation=0):
    """
    Return list of move directions for the agent.
    """
    # state = {0: 'up', 90: 'right', 180: 'down', -90: 'left'}.get(rotation)
    state = 'up'
    states = []
    rotations = []
    (x_prev, y_prev) = path[0]

    for x, y in path[1:]:
        state, cost = count_cost((x_prev, y_prev), (x, y), state)

        if cost == -1:
            states.append('turn left')
        elif cost > 0:
            states.extend(['turn right'] * cost)

        states.append('straight')
        rotations.append(cost)
        (x_prev, y_prev) = (x, y)

    return states
