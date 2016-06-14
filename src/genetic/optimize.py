import genetic
from route import *


def optimize_route(objects, generations, crossover_chance, mutation_chance, population):
    """Return list of points ordered by genetic algorithm."""
    generator = RouteGenerator(objects)
    ga = genetic.GeneticAlgorithm(generator, crossover_chance, mutation_chance, population)

    print("\nINITIAL ROUTES")
    print ", ".join([str(int(route.get_length())) for route in ga.get_solutions()])

    # initial = [route.get_length() for route in ga.get_solutions()]
    # best_initial = min(initial)
    # while ga.get_best_solution().get_length() > best_initial * 0.5:  # step condition instead of generations number
    #     # print ga.get_best_solution().get_length(), best_initial
    #     ga.evolve()

    for i in range(generations):
        ga.evolve()

    print("\nLAST GENERATION")
    print ", ".join([str(int(route.get_length())) for route in ga.get_solutions()])

    best = ga.get_best_solution()
    print("\nLENGTH OF ROUTE AFTER OPTIMIZATION")
    print int(best.get_length())

    return best.objects
