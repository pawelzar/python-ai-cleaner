def draw_point(graph, point, style):
    """Return single element with applied style."""
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
    """Print nice looking grid with all its elements.

    Style arguments:
    - number - print total path cost for each point
    - point_to - print direction for each point
    - path - print reconstructed path
    - start - print special character for start point
    - goal - print special character for goal point
    """
    for y in range(graph.height):
        print("".join(draw_point(graph, (x, y), style) for x in range(graph.width)))
