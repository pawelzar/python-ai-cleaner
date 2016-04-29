def draw_point(graph, point, style):
    r = "-"
    if point in graph.objects: r = graph.objects[point]
    if point in graph.obstacles: r = graph.obstacles[point]
    if point == graph.agent.position: r = "A"
    if 'number' in style and point in style['number']: r = style['number'][point]
    if 'point_to' in style and style['point_to'].get(point, None) is not None:
        (x1, y1) = point
        (x2, y2) = style['point_to'][point]
        if x2 == x1 + 1: r = "R"
        if x2 == x1 - 1: r = "L"
        if y2 == y1 + 1: r = "D"
        if y2 == y1 - 1: r = "U"
    if 'path' in style and point in style['path']: r = "@"
    if 'start' in style and point == style['start']: r = "A"
    if 'goal' in style and point == style['goal']: r = "Z"
    return "{} ".format(r)


def draw_grid(graph, **style):
    for y in range(graph.height):
        print("".join(draw_point(graph, (x, y), style) for x in range(graph.width)))
