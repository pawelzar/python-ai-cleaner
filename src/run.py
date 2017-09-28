import pygame

from core.classification import Classification
from core.neuron import NeuralNetwork
from model.cleaner import Cleaner
from model.gameboard import GameBoard
from model.object import Object
from settings import (
    CELL_MARGIN, CELL_HEIGHT, CELL_WIDTH, DIR_DOWN, DIR_LEFT,
    DIR_RIGHT, DIR_UP, GRID_HEIGHT, GRID_WIDTH, SCREEN_SIZE
)
from utils import file_path


# Initialize neural network
NETWORK = NeuralNetwork()


# Initialize classification (creates decision tree based on training set)
CLASSIFICATION = Classification(
    file_path('media.training_sets', 'train_cleaning'),
    file_path('media.training_sets', 'train_refill'),
)
CLASSIFICATION.draw_cleaning_tree()
CLASSIFICATION.draw_refill_tree()


# Initialize display
pygame.init()
pygame.display.set_caption('PRO CLEANER 9000')
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
CLOCK = pygame.time.Clock()


# Load paths of images
IMAGES = {
    'floor': file_path('media.images', 'floor_cell.jpg'),
    'agent': file_path('media.images', 'cleaner.png'),
    'bin': file_path('media.images', 'bin.png'),
    'station': file_path('media.images', 'station.png'),
    'sofa': file_path('media.images', 'furniture_sofa.png'),
    'chair': file_path('media.images', 'furniture_chair.png'),
    'desk': file_path('media.images', 'furniture_desk.png'),
    'palm': file_path('media.images', 'palm.png'),
    'dust': file_path('media.images', 'dirt_dust.png'),
    'water': file_path('media.images', 'dirt_water.png'),
    'cat': file_path('media.images', 'dirt_cat.png'),
}


# Load every image, use transparency for png images
LOADED_IMAGES = {
    name: pygame.image.load(path).convert_alpha()
    for name, path in IMAGES.items()
}


# Load special images (with rotation, scaled)
LOADED_IMAGES['chair_left'] = pygame.transform.rotate(
    pygame.image.load(IMAGES['chair']).convert_alpha(), -90
)
LOADED_IMAGES['chair_right'] = pygame.transform.rotate(
    pygame.image.load(IMAGES['chair']).convert_alpha(), 90
)
LOADED_IMAGES['floor'] = pygame.transform.scale(
    pygame.image.load(IMAGES['floor']).convert_alpha(),
    (CELL_WIDTH - CELL_MARGIN, CELL_HEIGHT - CELL_MARGIN)
)


# Initialize board
BOARD = GameBoard(GRID_WIDTH, GRID_HEIGHT)


# Add objects to the board
BOARD.add_furniture([
    Object('chair', (0, 3), LOADED_IMAGES['chair'].get_size()),
    Object('chair_left', (7, 5), LOADED_IMAGES['chair_left'].get_size()),
    Object('chair_right', (15, 5), LOADED_IMAGES['chair_right'].get_size()),
    Object('sofa', (9, 8), LOADED_IMAGES['sofa'].get_size()),
    Object('desk', (10, 2), LOADED_IMAGES['desk'].get_size()),
    Object('palm', (17, 1), LOADED_IMAGES['palm'].get_size()),
    Object('palm', (17, 9), LOADED_IMAGES['palm'].get_size()),
])
BOARD.add_station(
    Object('station', (0, 0), LOADED_IMAGES['station'].get_size())
)
BOARD.add_bin(
    Object('bin', (0, GRID_HEIGHT - 1), LOADED_IMAGES['bin'].get_size())
)

BOARD.assign_images(LOADED_IMAGES)
BOARD.assign_screen(SCREEN)


# Initialize cleaner
AGENT = Cleaner('agent', (0, 0), IMAGES['agent'])
AGENT.initialize(BOARD, SCREEN, NETWORK, CLASSIFICATION, IMAGES)


# Add dirt objects at random positions (number of objects as parameter)
BOARD.generate_random_dirt(15)

BOARD.assign_agent(AGENT)
BOARD.print_in_console()

PLAY = True


# Main loop of the program
while PLAY:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            PLAY = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                PLAY = False

            if event.key == pygame.K_UP:
                AGENT.move(DIR_UP)

            if event.key == pygame.K_DOWN:
                AGENT.move(DIR_DOWN)

            if event.key == pygame.K_LEFT:
                AGENT.move(DIR_LEFT)

            if event.key == pygame.K_RIGHT:
                AGENT.move(DIR_RIGHT)

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

            # Present the A* algorithm (show agent moves on path)
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
                BOARD.generate_random_dirt(20)

            if event.key == pygame.K_F9:
                AGENT.clean()

            if event.key == pygame.K_F10:
                AGENT.clean_next()

            # Turn automatic cleaning ON / OFF
            if event.key == pygame.K_F11:
                AGENT.set_cleaning()

            # Fill board randomly and immediately activate cleaning
            if event.key == pygame.K_F12:
                AGENT.generate_and_clean(20)

    BOARD.draw()
    AGENT.draw()

    CLOCK.tick(60)  # frames per second
    pygame.display.update()

pygame.quit()
