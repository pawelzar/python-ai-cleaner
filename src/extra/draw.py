def draw_point(graph, point, style):
    """Return single element with applied style."""
    sign = "-"
    if point in graph.objects: sign = graph.objects[point]
    if point in graph.obstacles: sign = graph.obstacles[point]
    if point == graph.station.position: sign = "S"
    if point == graph.agent.position: sign = "A"
    if point == graph.basket.position: sign = "B"
    if 'path' in style and point in style['path']: sign = "@"
    if 'start' in style and point == style['start']: sign = "A"
    if 'goal' in style and point == style['goal']: sign = "Z"
    return "{} ".format(sign)


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


def draw_tree(tree):
    for i, node in enumerate(str(tree).split('{')):
        print str(node).strip('}')
