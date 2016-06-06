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


class GameBoard(GridWithWeights):
    def __init__(self, width, height):
        super(GameBoard, self).__init__(width, height)
        self.furniture = []
        self.dirt = []
        self.agent = None

    def add_furniture(self, furniture):
        """Add object to the board that the agent can not pass through."""
        self.furniture.append(furniture)
        for row in range(furniture.get_width()):
            for column in range(furniture.get_height()):
                self.add_obstacle((furniture.pos_x() + row, furniture.pos_y() + column))

    def add_dirt(self, dirt):
        """Add dirt object to the board."""
        self.dirt.append(dirt)

    def add_agent(self, agent):
        """Assign agent to the board."""
        self.agent = agent

    def get_object_name(self, position):
        for item in self.dirt:
            if item.position == position:
                return item.name

    def get_points(self):
        return self.obstacles.keys() + [item.position for item in self.dirt]

    def get_furniture_points(self):
        return sorted(self.obstacles.keys())

    def get_dirt_points(self):
        return [item.position for item in self.dirt]

    def clean_object(self, position):
        for i, item in enumerate(self.dirt):
            if item.position == position:
                del self.dirt[i]
                del self.objects[position]
                del self.weights[position]
