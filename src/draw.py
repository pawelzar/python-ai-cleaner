def draw_tile(graph, id, style, width):
    r = "-"
    if id in graph.objects: r = graph.objects[id] * width
    if id in graph.obstacles: r = graph.obstacles[id] * width
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
    return r + " "


def draw_grid(graph, width=1, **style):
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width), end="")
        print()
