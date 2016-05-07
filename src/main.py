from random import randrange

import pygame

from src.algorithm import *
from src.draw import *
from src.graph import *
from src.object import *


# Initialize display
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("PRO CLEANER 9000")
clock = pygame.time.Clock()


# Load images
cleaner_image = pygame.image.load("../images/cleaner.png").convert_alpha()
cell_image = pygame.image.load("../images/floor_cell.jpg").convert_alpha()
cell_image = pygame.transform.scale(cell_image, (CELL_WIDTH - CELL_MARGIN, CELL_HEIGHT - CELL_MARGIN))

chair_image = pygame.image.load("../images/furniture_chair.png").convert_alpha()
chair_left_image = pygame.transform.rotate(chair_image, -90)
chair_right_image = pygame.transform.rotate(chair_image, 90)
sofa_image = pygame.image.load("../images/furniture_sofa.png").convert_alpha()
desk_image = pygame.image.load("../images/furniture_desk.png").convert_alpha()
palm_image = pygame.image.load("../images/palm.png").convert_alpha()

dirt_dust_image = pygame.image.load("../images/dirt_dust.png").convert_alpha()
dirt_water_image = pygame.image.load("../images/dirt_water.png").convert_alpha()
dirt_cat_image = pygame.image.load("../images/dirt_cat.png").convert_alpha()

images = {
    "agent": cleaner_image,
    "floor": cell_image,
    "sofa": sofa_image,
    "chair": chair_image,
    "chair_left": chair_left_image,
    "chair_right": chair_right_image,
    "desk": desk_image,
    "palm": palm_image,

    "dust": dirt_dust_image,
    "water": dirt_water_image,
    "cat": dirt_cat_image
}


# Initialize board
BOARD = GameBoard(NUM_COLS, NUM_ROWS)


# Add objects to the game board
BOARD.add_furniture(Object("chair", (0, 3), images["chair"].get_size()))
BOARD.add_furniture(Object("chair_left", (17, 7), images["chair_left"].get_size()))
BOARD.add_furniture(Object("chair_right", (5, 5), images["chair_right"].get_size()))
BOARD.add_furniture(Object("sofa", (10, 10), images["sofa"].get_size()))
BOARD.add_furniture(Object("desk", (10, 2), images["desk"].get_size()))
BOARD.add_furniture(Object("palm", (5, 16), images["palm"].get_size()))
BOARD.add_furniture(Object("palm", (15, 15), images["palm"].get_size()))
BOARD.add_furniture(Object("palm", (19, 17), images["palm"].get_size()))
BOARD.add_furniture(Object("palm", (25, 8), images["palm"].get_size()))
BOARD.add_agent(Object("agent", (0, 0)))


position_dirt_dust = [(randrange(0, NUM_COLS, 1), randrange(0, NUM_ROWS, 1)) for _ in range(30)]
position_dirt_water = [(randrange(0, NUM_COLS, 1), randrange(0, NUM_ROWS, 1)) for _ in range(30)]
position_dirt_cat = [(randrange(0, NUM_COLS, 1), randrange(0, NUM_ROWS, 1)) for _ in range(30)]

for x, y in position_dirt_dust:
    BOARD.add_object((x, y), '1')
    BOARD.add_weight((x, y), 20)
    BOARD.add_dirt(Object("dust", (x, y)))

for x, y in position_dirt_water:
    BOARD.add_object((x, y), '2')
    BOARD.add_weight((x, y), 5)
    BOARD.add_dirt(Object("water", (x, y)))

for x, y in position_dirt_cat:
    BOARD.add_object((x, y), '3')
    BOARD.add_weight((x, y), 10)
    BOARD.add_dirt(Object("cat", (x, y)))


print("INITIAL GAME BOARD")
draw_grid(BOARD)
point_goal = (0, 8)
play = True


# Main loop of the program
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if BOARD.agent.pos_x() > 0:
                    BOARD.agent.move(-1, 0)

            if event.key == pygame.K_RIGHT:
                if BOARD.agent.pos_x() < NUM_COLS - 1:
                    BOARD.agent.move(1, 0)

            if event.key == pygame.K_UP:
                if BOARD.agent.pos_y() > 0:
                    BOARD.agent.move(0, -1)

            if event.key == pygame.K_DOWN:
                if BOARD.agent.pos_y() < NUM_ROWS - 1:
                    BOARD.agent.move(0, 1)

            # Some predefined position settings
            if event.key == pygame.K_1:
                BOARD.agent.position = (0, 0)
                point_goal = (0, 8)

            if event.key == pygame.K_2:
                BOARD.agent.position = (11, 8)
                point_goal = (11, 13)

            if event.key == pygame.K_3:
                BOARD.agent.position = (0, 0)
                point_goal = (11, 13)

            # Present the work of the algorithm
            if event.key == pygame.K_END:
                came_from, cost_so_far = a_star_search(BOARD, BOARD.agent.position, point_goal)
                reconstruction = reconstruct_path(came_from, start=BOARD.agent.position, goal=point_goal)

                print("\nPATH FROM POINT {} to {}".format(BOARD.agent.position, point_goal))
                draw_grid(BOARD, path=reconstruction, start=BOARD.agent.position, goal=point_goal)

                print("\nPATH AS STATES")
                print(", ".join(path_as_states(reconstruction)))

                for x, y in reconstruction:
                    screen.blit(images["agent"], (x * CELL_WIDTH, y * CELL_HEIGHT))
                    pygame.display.flip()
                    pygame.time.wait(100)

                BOARD.agent.position = point_goal

            if event.key == pygame.K_HOME:
                print("\nCURRENT GAME BOARD")
                draw_grid(BOARD)

    # Set the screen background
    screen.fill(GREY)

    # Draw the grid
    for row in range(NUM_ROWS):
        for column in range(NUM_COLS):
            screen.blit(images["floor"], [column * CELL_WIDTH + CELL_MARGIN / 2, row * CELL_HEIGHT + CELL_MARGIN / 2])

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
