from src.algorithm import *
from src.graph import *


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
    if id in graph.obstacles: r = graph.obstacles[id] * width
    if id in graph.objects: r = graph.objects[id] * width
    return r


def draw_grid(graph, width=1, **style):
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width), end="")
        print()


diagram = SquareGrid(10, 10)
diagram.add_obstacle([(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8), (1, 1), (1, 2), (2, 1), (2, 2)])
diagram.add_object((5, 5), '1')

point_start = (0, 0)
point_goal = (4, 8)
came_from, cost_so_far = a_star_search(diagram, point_start, point_goal)

draw_grid(diagram, point_to=came_from, start=point_start, goal=point_goal)
print()
draw_grid(diagram, number=cost_so_far, start=point_start, goal=point_goal)
print()
draw_grid(diagram, path=reconstruct_path(came_from, start=point_start, goal=point_goal))
print(reconstruct_path(came_from, start=point_start, goal=point_goal))
