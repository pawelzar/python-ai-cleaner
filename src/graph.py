class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = {}
        self.objects = {}

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.obstacles

    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def add_obstacle(self, points):
        for x in points:
            self.obstacles[x] = '#'

    def add_object(self, point, character):
        self.objects[point] = character


class GridWithWeights(Grid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

    def add_weight(self, point, weight):
        self.weights[point] = weight
