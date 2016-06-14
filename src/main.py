import pygame

from src.core.classification import Classification
from src.core.neuron import NeuralNetwork
from src.extra.settings import *
from src.structure.cleaner import Cleaner
from src.structure.gameboard import GameBoard
from src.structure.object import Object
from src.genetic.optimize import optimize_route

# Initialize neural network
network = NeuralNetwork()

# Initialize classification (creates decision tree based on training set)
classification = Classification("train_cleaning", "train_refill")
classification.draw_cleaning_tree()
classification.draw_refill_tree()

# Initialize display
pygame.init()
pygame.display.set_caption("PRO CLEANER 9000")
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

# Load paths of images
img_path = {
    "floor": "../images/floor_cell.jpg",
    "agent": "../images/cleaner.png",
    "bin": "../images/bin.png",
    "station": "../images/station.png",
    "sofa": "../images/furniture_sofa.png",
    "chair": "../images/furniture_chair.png",
    "desk": "../images/furniture_desk.png",
    "palm": "../images/palm.png",
    "dust": "../images/dirt_dust.png",
    "water": "../images/dirt_water.png",
    "cat": "../images/dirt_cat.png"
}

# Load every image, use transparency for png images
images = {name: pygame.image.load(path).convert_alpha() for name, path in img_path.items()}

# Load special images (with rotation, scaled)
images["chair_left"] = pygame.transform.rotate(
    pygame.image.load("../images/furniture_chair.png").convert_alpha(), -90)
images["chair_right"] = pygame.transform.rotate(
    pygame.image.load("../images/furniture_chair.png").convert_alpha(), 90)
images["floor"] = pygame.transform.scale(
    pygame.image.load("../images/floor_cell.jpg").convert_alpha(),
    (CELL_WIDTH - CELL_MARGIN, CELL_HEIGHT - CELL_MARGIN))

# Initialize board
BOARD = GameBoard(WIDTH, HEIGHT)

# Add objects to the board
BOARD.add_furniture(Object("chair", (0, 3), images["chair"].get_size()))
BOARD.add_furniture(Object("chair_left", (7, 5), images["chair_left"].get_size()))
BOARD.add_furniture(Object("chair_right", (15, 5), images["chair_right"].get_size()))
BOARD.add_furniture(Object("sofa", (9, 8), images["sofa"].get_size()))
BOARD.add_furniture(Object("desk", (10, 2), images["desk"].get_size()))
BOARD.add_furniture(Object("palm", (17, 1), images["palm"].get_size()))
BOARD.add_furniture(Object("palm", (17, 9), images["palm"].get_size()))
BOARD.add_station(Object("station", (0, 0), images["station"].get_size()))
BOARD.add_bin(Object("bin", (0, HEIGHT-1), images["bin"].get_size()))
BOARD.assign_images(images)
BOARD.assign_screen(screen)

# Initialize cleaner
AGENT = Cleaner("agent", (0, 0), img_path["agent"])
AGENT.assign_board(BOARD)
AGENT.assign_screen(screen)
AGENT.assign_network(network)
AGENT.assign_classification(classification)
AGENT.assign_images(img_path)

# Add objects of type dirt at random positions (number of objects as parameter)
BOARD.generate_random_dirt(15)

BOARD.assign_agent(AGENT)
BOARD.print_in_console()
PLAY = True

route = optimize_route(BOARD.get_dirt_points(), GENERATIONS, CROSSOVER_CHANCE, MUTATION_CHANCE, POPULATION)
# Main loop of the program
while PLAY:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            PLAY = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                AGENT.move(UP)

            if event.key == pygame.K_DOWN:
                AGENT.move(DOWN)

            if event.key == pygame.K_LEFT:
                AGENT.move(LEFT)

            if event.key == pygame.K_RIGHT:
                AGENT.move(RIGHT)

            # Some predefined position settings
            if event.key == pygame.K_1:
                AGENT.position = (0, 0)
                BOARD.point_goal = (0, 8)

            if event.key == pygame.K_2:
                AGENT.position = (11, 7)
                BOARD.point_goal = (11, 11)

            if event.key == pygame.K_3:
                AGENT.position = (0, 0)
                BOARD.point_goal = (11, 11)

            # Print nice looking grid in console
            if event.key == pygame.K_HOME:
                BOARD.print_in_console()

            # Present the A* algorithm (show agent movements on path)
            if event.key == pygame.K_END:
                AGENT.move_to(BOARD.point_goal)

            if event.key == pygame.K_F1:
                AGENT.recognize()

            if event.key == pygame.K_F2:
                AGENT.collect_data()

            if event.key == pygame.K_F3:
                AGENT.go_to_station()

            if event.key == pygame.K_F4:
                AGENT.reload()

            if event.key == pygame.K_F5:
                AGENT.empty_container()

            if event.key == pygame.K_F6:
                BOARD.generate_random_dirt(12)

            if event.key == pygame.K_F9:
                AGENT.clean()

            if event.key == pygame.K_F10:
                AGENT.clean_next()

            # Turn automatic cleaning ON / OFF
            if event.key == pygame.K_F11:
                AGENT.set_cleaning()

            # Fill board randomly and immediately activate cleaning
            if event.key == pygame.K_F12:
                AGENT.generate_and_clean(12)

    BOARD.draw()
    AGENT.draw()

    clock.tick(60)  # frames per second
    pygame.display.update()

pygame.quit()
