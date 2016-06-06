from random import randrange

import pygame
import cv2

from algorithm import *
from draw import *
from graph import *
from object import *
from neuron import NeuralNetwork, NeuralTest, NeuralTrain


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
#BOARD.add_furniture(Object("palm", (19, 17), images["palm"].get_size()))
#BOARD.add_furniture(Object("palm", (25, 8), images["palm"].get_size()))
BOARD.add_furniture(Object("station", (0, 0), images["station"].get_size()))
BOARD.add_agent(Object("agent", (0, 0)))


for i in range(10):
    (x, y) = (randrange(0, NUM_COLS, 1), randrange(0, NUM_ROWS, 1))
    while (x, y) in BOARD.get_points():
        (x, y) = (randrange(0, NUM_COLS, 1), randrange(0, NUM_ROWS, 1))

    BOARD.add_object((x, y), '1')
    BOARD.add_weight((x, y), 20)
    BOARD.add_dirt(Object("dust", (x, y)))


for i in range(10):
    (x, y) = (randrange(0, NUM_COLS, 1), randrange(0, NUM_ROWS, 1))
    while (x, y) in BOARD.get_points():
        (x, y) = (randrange(0, NUM_COLS, 1), randrange(0, NUM_ROWS, 1))

    BOARD.add_object((x, y), '2')
    BOARD.add_weight((x, y), 5)
    BOARD.add_dirt(Object("water", (x, y)))


for i in range(10):
    (x, y) = (randrange(0, NUM_COLS, 1), randrange(0, NUM_ROWS, 1))
    while (x, y) in BOARD.get_points():
        (x, y) = (randrange(0, NUM_COLS, 1), randrange(0, NUM_ROWS, 1))

    BOARD.add_object((x, y), '3')
    BOARD.add_weight((x, y), 10)
    BOARD.add_dirt(Object("cat", (x, y)))

#print str(BOARD.get_furniture_points())
#print str(BOARD.get_dirt_points())


print("INITIAL GAME BOARD")
draw_grid(BOARD)
point_goal = (0, 8)
play = True


def display_refresh(BOARD):
    # Set the screen background
    screen.fill(GREY)

    # Draw the grid
    for row in range(NUM_ROWS):
        for column in range(NUM_COLS):
            screen.blit(images["floor"], [column * CELL_WIDTH + (CELL_MARGIN / 2),
                                          row * CELL_HEIGHT + (CELL_MARGIN / 2)])

    # Draw board elements
    for dirt in BOARD.dirt:
        screen.blit(images[dirt.name], dirt.real_position())

    for furniture in BOARD.furniture:
        screen.blit(images[furniture.name], furniture.real_position())

    screen.blit(images["agent"], BOARD.agent.real_position())


# Main loop of the program
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if BOARD.agent.pos_y() > 0:
                    BOARD.agent.move(0, -1)

            if event.key == pygame.K_DOWN:
                if BOARD.agent.pos_y() < NUM_ROWS - 1:
                    BOARD.agent.move(0, 1)

            if event.key == pygame.K_LEFT:
                if BOARD.agent.pos_x() > 0:
                    BOARD.agent.move(-1, 0)

            if event.key == pygame.K_RIGHT:
                if BOARD.agent.pos_x() < NUM_COLS - 1:
                    BOARD.agent.move(1, 0)

            # Some predefined position settings
            if event.key == pygame.K_1:
                BOARD.agent.position = (0, 0)
                point_goal = (0, 8)

            if event.key == pygame.K_2:
                BOARD.agent.position = (11, 7)
                point_goal = (11, 11)

            if event.key == pygame.K_3:
                BOARD.agent.position = (0, 0)
                point_goal = (11, 11)

            # Present the work of the algorithm
            if event.key == pygame.K_END:
                came_from, cost_so_far = a_star_search(BOARD, BOARD.agent.position, point_goal, 'up')
                reconstruction = reconstruct_path(came_from, start=BOARD.agent.position, goal=point_goal)

                print("\nPATH FROM POINT {} to {}".format(BOARD.agent.position, point_goal))
                draw_grid(BOARD, path=reconstruction, start=BOARD.agent.position, goal=point_goal)

                print("\nORDERS FOR AGENT TO MOVE")
                print(", ".join(str(x) for x in path_as_orders(reconstruction)))

                directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # [up, right, down, left]
                direction = 0
                rotation = 0
                for order in path_as_orders(reconstruction):
                    if order == 'turn right':
                        rotation -= 90
                        images["agent"] = pygame.transform.rotate(images["agent"], -90)
                        direction = (direction + 1) % 4
                    elif order == 'turn left':
                        rotation += 90
                        images["agent"] = pygame.transform.rotate(images["agent"], 90)
                        direction = (direction - 1) % 4
                    else:
                        BOARD.agent.move(*directions[direction])

                    screen.blit(images["agent"], BOARD.agent.real_position())
                    pygame.display.flip()
                    pygame.time.wait(100)

                images["agent"] = pygame.transform.rotate(images["agent"], -rotation)

            if event.key == pygame.K_BACKSPACE:
                image = img_path.get(BOARD.get_object_name(BOARD.agent.position), "")
                if image:
                    test = NeuralTest(cv2.imread(image))
                    test.prepare_test_data()
                    recognition = network.test_network(test)
                    print(recognition)
                    # print BOARD.get_object_name(BOARD.agent.position)
                else:
                    print("None")

            if event.key == pygame.K_c:
                BOARD.clean_object(BOARD.agent.position)
                draw_grid(BOARD)

            if event.key == pygame.K_0:
                #distances = sorted(map(lambda a, b: heuristic(a, b),
                #                [(BOARD.agent.position, item.position) for item in BOARD.dirt]))
                while BOARD.dirt:
                    point_goal = BOARD.agent.find_closest(BOARD)
                    came_from, cost_so_far = a_star_search(BOARD, BOARD.agent.position, point_goal, 'up')
                    reconstruction = reconstruct_path(came_from, start=BOARD.agent.position, goal=point_goal)

                    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # [up, right, down, left]
                    direction = 0
                    rotation = 0
                    for order in path_as_orders(reconstruction):
                        if order == 'turn right':
                            rotation -= 90
                            images["agent"] = pygame.transform.rotate(images["agent"], -90)
                            direction = (direction + 1) % 4
                        elif order == 'turn left':
                            rotation += 90
                            images["agent"] = pygame.transform.rotate(images["agent"], 90)
                            direction = (direction - 1) % 4
                        else:
                            BOARD.agent.move(*directions[direction])

                        #screen.blit(images["agent"], BOARD.agent.real_position())
                        display_refresh(BOARD)
                        pygame.display.flip()
                        pygame.time.wait(100)

                    BOARD.clean_object(BOARD.agent.position)
                    images["agent"] = pygame.transform.rotate(images["agent"], -rotation)

            if event.key == pygame.K_HOME:
                print("\nCURRENT GAME BOARD")
                draw_grid(BOARD)

    # Set the screen background
    screen.fill(GREY)

    # Draw the grid
    for row in range(NUM_ROWS):
        for column in range(NUM_COLS):
            screen.blit(images["floor"], [column * CELL_WIDTH + (CELL_MARGIN / 2),
                                          row * CELL_HEIGHT + (CELL_MARGIN / 2)])

    # Draw board elements
    for dirt in BOARD.dirt:
        screen.blit(images[dirt.name], dirt.real_position())

    for furniture in BOARD.furniture:
        screen.blit(images[furniture.name], furniture.real_position())

    # Draw crossed lines at the target point
    pygame.draw.line(screen, GREY, ((point_goal[0] + 0.5) * CELL_WIDTH - 1, point_goal[1] * CELL_HEIGHT),
                     ((point_goal[0] + 0.5) * CELL_WIDTH - 1, (point_goal[1] + 1) * CELL_HEIGHT - 1), 4)
    pygame.draw.line(screen, GREY, (point_goal[0] * CELL_WIDTH, (point_goal[1] + 0.5) * CELL_HEIGHT - 1),
                     ((point_goal[0] + 1) * CELL_WIDTH - 1, (point_goal[1] + 0.5) * CELL_HEIGHT - 1), 4)

    screen.blit(images["agent"], BOARD.agent.real_position())

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
