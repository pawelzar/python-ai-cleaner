import math
import random
from src.core.algorithm import euclidean


class Route:
    def __init__(self, objects):
        self.objects = objects

    @staticmethod
    def distance(obj_1, obj_2):
        """Calculate the distance between two objects. (Euclidean distance)"""
        # return heuristic(city1, city2)
        # return len(a_star_search(grid, city1, city2))
        # return math.hypot(city2[0] - city1[0], city2[1] - city1[1])
        return euclidean(obj_1, obj_2)

    def get_length(self):
        """Calculate the length of the route."""
        # print self.objects
        return sum([self.distance(self.objects[i - 1], self.objects[i]) for i in range(len(self.objects))])

    def get_fitness(self):
        return 1 / self.get_length()

    def crossover(self, route):
        x1 = len(self.objects) / 3
        x2 = x1 * 2
        part = self.objects[x1:x2]

        temp = []
        i = 0
        while len(temp) < x1:
            if route.objects[i] not in part:
                temp.append(route.objects[i])
            i += 1
        temp.extend(part)

        while len(temp) < len(route.objects):
            if route.objects[i] not in temp:
                temp.append(route.objects[i])
            i += 1

        route = temp

    def mutate(self):
        """Swap two objects."""
        index_1 = random.randint(0, len(self.objects) - 1)
        index_2 = random.randint(0, len(self.objects) - 1)
        self.objects[index_1], self.objects[index_2] = self.objects[index_2], self.objects[index_1]

    def copy(self):
        return Route(self.objects[:])


class RouteGenerator:
    def __init__(self, objects):
        self.objects = objects

    def generate(self):
        objects = self.objects[:]
        random.shuffle(objects)
        return Route(objects)
