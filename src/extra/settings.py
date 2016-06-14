# Define some colors
BLACK = (0, 0, 0)
DARK = (40, 40, 40)
GREY = (80, 80, 80)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions for moving ((0, 0) in top left corner)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Set number of rows (HEIGHT) and columns (WIDTH) in the grid
WIDTH = 20
HEIGHT = 12

# Set width and height of cell in the grid (in pixels)
CELL_WIDTH = 30
CELL_HEIGHT = 30

# Set margin between each cell (in pixels)
CELL_MARGIN = 1

# Set width and height of the screen (in pixels)
SCREEN_SIZE = [CELL_WIDTH * WIDTH, CELL_HEIGHT * HEIGHT]


# SETTINGS FOR GENETIC ALGORITHMS

# The number of routes in each generation
POPULATION = 5

# Number of generations
GENERATIONS = 1000

# The change a crossover happens for every 2 routes that go from the old generation to the next
CROSSOVER_CHANCE = 0.7

# The change of a mutation for each route that goes from the old generation to the next
MUTATION_CHANCE = 0.5
