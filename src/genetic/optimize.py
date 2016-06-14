import genetic
from route import *


def optimize_route(objects, generations, crossover_chance, mutation_chance, population):
    """Return list of points ordered by genetic algorithm."""
    generator = RouteGenerator(objects)
    ga = genetic.GeneticAlgorithm(generator, crossover_chance, mutation_chance, population)
    print("\nINITIAL LENGTHS OF ROUTES")
    print [route.get_length() for route in ga.get_solutions()]

    for i in range(generations):
        ga.evolve()

    best = ga.get_best_solution()
    print("\nLENGTH OF ROUTE AFTER OPTIMIZATION.")
    print best.get_length()

    return best.objects
