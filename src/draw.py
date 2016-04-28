def draw_line(graph, id, style):
    r = "-"
    if id in graph.objects: r = graph.objects[id]
    if id in graph.obstacles: r = graph.obstacles[id]
    if 'number' in style and id in style['number']: r = style['number'][id]
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
    return "{} ".format(r)


def draw_grid(graph, **style):
    for y in range(graph.height):
        for x in range(graph.width):
            print(draw_line(graph, (x, y), style), end="")
        print()
