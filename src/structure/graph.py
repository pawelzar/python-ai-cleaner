class Grid(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = {}
        self.objects = {}

    def in_bounds(self, point):
        """Return whether point is located inside the board."""
        (x, y) = point
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, point):
        """Return whether the agent may go through the point."""
        return point not in self.obstacles

    def neighbors(self, point):
        """Return closest points (distanced by 1 cell in every direction) through which the agent may go."""
        (x, y) = point
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def add_obstacle(self, point):
        """Specify the point through which the agent can not go."""
        self.obstacles[point] = '#'

    def add_object(self, point, character):
        """Assign the character to the given point on the board."""
        self.objects[point] = character


class GridWithWeights(Grid):
    def __init__(self, width, height):
        super(GridWithWeights, self).__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        """Return weight of the node, if none return 1."""
        return self.weights.get(to_node, 1)

    def add_weight(self, point, weight):
        """Assign the weight to the given point on the board."""
        self.weights[point] = weight
