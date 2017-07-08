import random
from core.algorithm import euclidean, heuristic


class Route:
    def __init__(self, objects):
        self.objects = objects

    @staticmethod
    def distance(obj_1, obj_2):
        """
        Calculate the distance between two objects.
        """
        # return heuristic(obj_1, obj_2)
        return euclidean(obj_1, obj_2)

    def get_length(self):
        """
        Calculate the length of the route.
        """
        # print self.objects
        return sum([
            self.distance(self.objects[i - 1], self.objects[i])
            for i in range(len(self.objects))
        ])

    def get_fitness(self):
        return 1 / self.get_length()

    def crossover(self, route):
        """
        Copy selected part from one parent to another (given as route)
        in the same place.
        """
        x_1 = len(self.objects) / 3
        x_2 = x_1 * 2
        part = self.objects[x_1:x_2]

        temp = []
        index = 0
        while len(temp) < x_1:
            if route.objects[index] not in part:
                temp.append(route.objects[index])
            index += 1
        temp.extend(part)

        while len(temp) < len(route.objects):
            if route.objects[index] not in temp:
                temp.append(route.objects[index])
            index += 1

        route.objects = temp

    def mutate(self):
        """
        Swap two objects.
        """
        index_1 = random.randint(0, len(self.objects) - 1)
        index_2 = random.randint(0, len(self.objects) - 1)
        self.objects[index_1], self.objects[index_2] = (
            self.objects[index_2], self.objects[index_1]
        )

    def copy(self):
        return Route(self.objects[:])


class RouteGenerator:
    def __init__(self, objects):
        self.objects = objects

    def generate(self):
        objects = self.objects[:]
        random.shuffle(objects)
        return Route(objects)
