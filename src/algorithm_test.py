from src.algorithm import *
from src.grid import *


def draw_tile(graph, id, style, width):
    r = "."
    if 'number' in style and id in style['number']: r = "%d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = "R"
        if x2 == x1 - 1: r = "L"
        if y2 == y1 + 1: r = "D"
        if y2 == y1 - 1: r = "U"
    if 'start' in style and id == style['start']: r = "A"
    if 'goal' in style and id == style['goal']: r = "Z"
    if 'path' in style and id in style['path']: r = "@"
    if id in graph.walls: r = "#" * width
    return r


def draw_grid(graph, width=2, **style):
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width), end="")
        print()

diagram = GridWithWeights(10, 10)
diagram.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8), (1, 1), (1, 2), (2, 1), (2, 2)]
diagram.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
                                      (4, 3), (4, 4), (4, 5), (4, 6),
                                      (4, 7), (4, 8), (5, 1), (5, 2),
                                      (5, 3), (5, 4), (5, 5), (5, 6),
                                      (5, 7), (5, 8), (6, 2), (6, 3),
                                      (6, 4), (6, 5), (6, 6), (6, 7),
                                      (7, 3), (7, 4), (7, 5)]}

point_start = (0, 0)
point_goal = (4, 8)
came_from, cost_so_far = a_star_search(diagram, point_start, point_goal)

draw_grid(diagram, width=1, point_to=came_from, start=point_start, goal=point_goal)
print()
draw_grid(diagram, width=1, number=cost_so_far, start=point_start, goal=point_goal)
print()
draw_grid(diagram, width=1, path=reconstruct_path(came_from, start=point_start, goal=point_goal))
print(reconstruct_path(came_from, start=point_start, goal=point_goal))
