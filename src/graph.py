class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = {}
        self.objects = {}

    def in_bounds(self, point):
        (x, y) = point
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, point):
        return point not in self.obstacles

    def neighbors(self, point):
        (x, y) = point
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def add_obstacle(self, point):
        self.obstacles[point] = '#'

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


class GameBoard(GridWithWeights):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.furniture = []
        self.dirt = []
        self.agent = None

    def add_furniture(self, furniture):
        self.furniture.append(furniture)
        for row in range(furniture.get_width()):
            for column in range(furniture.get_height()):
                self.add_obstacle((furniture.pos_x() + row, furniture.pos_y() + column))

    def add_dirt(self, dirt):
        self.dirt.append(dirt)

    def add_agent(self, agent):
        self.agent = agent
