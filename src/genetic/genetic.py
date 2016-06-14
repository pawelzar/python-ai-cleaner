import random


class GeneticAlgorithm:
    def __init__(self, solution_generator, crossover_chance, mutation_chance, population):
        self.crossover_chance = crossover_chance
        self.mutation_chance = mutation_chance
        self.population = population
        self.generation = self.create_initial_population(solution_generator)

    def create_initial_population(self, solution_generator):
        """Generate as many routes as the number of population."""
        solutions = [solution_generator.generate() for i in range(self.population)]
        return solutions

    def get_solutions(self):
        """Return list of routes. Number of routes is the number of population."""
        return self.generation

    def get_best_solution(self):
        """Returns the solution that returns the highest fitness score."""
        all_fitness = [solution.get_fitness() for solution in self.generation]
        return self.generation[all_fitness.index(max(all_fitness))]

    def select(self, all_fitness):
        """Select a value from the array all_fitness on a random number
        based on the fitness values."""
        selection = random.random() * sum(all_fitness)

        index = 0
        while selection > 0:
            selection -= all_fitness[index]
            index += 1

        return self.generation[index - 1]

    def evolve(self):
        """Create new generation based on previous one.
        Some of the solutions have a crossover or mutation performed on them.
        """

        # Fitness calculation
        all_fitness = [solution.get_fitness() for solution in self.generation]
        floor = min(all_fitness)
        all_fitness = [fitness - floor for fitness in all_fitness]

        new_generation = []
        while len(new_generation) < len(self.generation):
            # Select two parents
            parents = [self.select(all_fitness).copy(), self.select(all_fitness).copy()]

            # Randomly run them through crossover()
            if random.random() <= self.crossover_chance:
                parents[0].crossover(parents[1])

            # Randomly run them through mutate()
            for parent in parents:
                if random.random() <= self.mutation_chance:
                    parent.mutate()

            # Add them to the new batch of routes.
            new_generation.extend(parents)

        # print "self gen", "\n".join(str(route.objects) for route in self.generation)
        # print "new gen", "\n".join(str(route.objects) for route in new_generation)
        self.generation = new_generation
