import pygame

from src.settings import *
from src.neuron import NeuralNetwork
from src.draw import draw_grid

from src.structure.cleaner import Cleaner
from src.structure.gameboard import GameBoard
from src.structure.object import Object


# Initialize neural network
network = NeuralNetwork()

# Initialize display
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("PRO CLEANER 9000")
clock = pygame.time.Clock()

# Load images
images = {
    "agent": pygame.image.load("../images/cleaner.png").convert_alpha(),
    "floor": pygame.transform.scale(pygame.image.load("../images/floor_cell.jpg").convert_alpha(),
                                    (CELL_WIDTH - CELL_MARGIN, CELL_HEIGHT - CELL_MARGIN)),
    "station": pygame.image.load("../images/station.png").convert_alpha(),
    "sofa": pygame.image.load("../images/furniture_sofa.png").convert_alpha(),
    "chair": pygame.image.load("../images/furniture_chair.png").convert_alpha(),
    "chair_left": pygame.transform.rotate(pygame.image.load("../images/furniture_chair.png").convert_alpha(), -90),
    "chair_right": pygame.transform.rotate(pygame.image.load("../images/furniture_chair.png").convert_alpha(), 90),
    "desk": pygame.image.load("../images/furniture_desk.png").convert_alpha(),
    "palm": pygame.image.load("../images/palm.png").convert_alpha(),

    "dust": pygame.image.load("../images/dirt_dust.png").convert_alpha(),
    "water": pygame.image.load("../images/dirt_water.png").convert_alpha(),
    "cat": pygame.image.load("../images/dirt_cat.png").convert_alpha()
}

img_path = {
    "dust": "../images/dirt_dust.png",
    "water": "../images/dirt_water.png",
    "cat": "../images/dirt_cat.png",
    "floor": "../images/floor_cell.jpg"
}

# Initialize board
BOARD = GameBoard(NUM_COLS, NUM_ROWS)

# Add objects to the game board
BOARD.add_furniture(Object("chair", (0, 3), images["chair"].get_size()))
BOARD.add_furniture(Object("chair_left", (7, 5), images["chair_left"].get_size()))
BOARD.add_furniture(Object("chair_right", (15, 5), images["chair_right"].get_size()))
BOARD.add_furniture(Object("sofa", (9, 8), images["sofa"].get_size()))
BOARD.add_furniture(Object("desk", (10, 2), images["desk"].get_size()))
BOARD.add_furniture(Object("palm", (17, 1), images["palm"].get_size()))
BOARD.add_furniture(Object("palm", (17, 9), images["palm"].get_size()))
BOARD.add_station(Object("station", (0, 0), images["station"].get_size()))
BOARD.assign_images(images)
BOARD.assign_screen(screen)

agent = Cleaner("agent", (0, 0))
agent.assign_board(BOARD)
agent.assign_screen(screen)
agent.assign_network(network)

# Add random dirt objects
BOARD.generate_random_dirt(10)

print("INITIAL GAME BOARD")
draw_grid(BOARD)
BOARD.point_goal = (0, 8)
play = True

# Main loop of the program
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if agent.pos_y() > 0:
                    agent.move(0, -1)

            if event.key == pygame.K_DOWN:
                if agent.pos_y() < NUM_ROWS - 1:
                    agent.move(0, 1)

            if event.key == pygame.K_LEFT:
                if agent.pos_x() > 0:
                    agent.move(-1, 0)

            if event.key == pygame.K_RIGHT:
                if agent.pos_x() < NUM_COLS - 1:
                    agent.move(1, 0)

            # Some predefined position settings
            if event.key == pygame.K_1:
                agent.position = (0, 0)
                BOARD.point_goal = (0, 8)

            if event.key == pygame.K_2:
                agent.position = (11, 7)
                BOARD.point_goal = (11, 11)

            if event.key == pygame.K_3:
                agent.position = (0, 0)
                BOARD.point_goal = (11, 11)

            # Print nic looking grid in console
            if event.key == pygame.K_HOME:
                print("\nCURRENT GAME BOARD")
                draw_grid(BOARD)

            # Present the A* algorithm (move on path)
            if event.key == pygame.K_END:
                agent.move_to(BOARD.point_goal)

            if event.key == pygame.K_F1:
                agent.recognize(img_path)

            if event.key == pygame.K_F2:
                agent.collect_data(img_path)

            if event.key == pygame.K_F3:
                agent.go_to_station()

            if event.key == pygame.K_F4:
                BOARD.generate_random_dirt(20)

            if event.key == pygame.K_F9:
                agent.clean()

            if event.key == pygame.K_F10:
                agent.clean_next()

            if event.key == pygame.K_F11:
                agent.set_to_cleaning()

            if event.key == pygame.K_F12:
                agent.create_and_clean(img_path)

    BOARD.draw()
    agent.draw()

    clock.tick(60)
    pygame.display.update()

pygame.quit()
