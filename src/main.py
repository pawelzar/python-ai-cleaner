import pygame

from draw import *
from graph import *
from screen_settings import *
from algorithm import *
from furniture import *
from random import randrange


# Initialize board
GRID = GameBoard(NUM_COLS, NUM_ROWS)


# Initialize display
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("PRO CLEANER 9000")
clock = pygame.time.Clock()


# Load images
cell_image = pygame.image.load("../images/floor_cell.jpg").convert_alpha()
cleaner_image = pygame.image.load("../images/cleaner.png").convert_alpha()

chair_image = pygame.image.load("../images/furniture_chair.png").convert_alpha()
sofa_image = pygame.image.load("../images/furniture_sofa.png").convert_alpha()

dirt_dust_image = pygame.image.load("../images/dirt_dust.png").convert_alpha()
dirt_water_image = pygame.image.load("../images/dirt_water.png").convert_alpha()
dirt_cat_image = pygame.image.load("../images/dirt_cat.png").convert_alpha()

images = {
    "sofa": sofa_image,
    "chair": chair_image,
    "agent": cleaner_image,

    "dust": dirt_dust_image,
    "water": dirt_water_image,
    "cat": dirt_cat_image
}


# Load furniture images
furniture_chair = Furniture(0, 90, "../images/furniture_chair.png")
furniture_sofa = Furniture(300, 300, "../images/furniture_sofa.png")
GRID.add_furniture(furniture_chair)
GRID.add_furniture(furniture_sofa)

position_cleaner = [0, 0]

position_dirt_dust = [(randrange(0, NUM_ROWS, 1), randrange(0, NUM_COLS, 1)) for _ in range(20)]
position_dirt_water = [(randrange(0, NUM_ROWS, 1), randrange(0, NUM_COLS, 1)) for _ in range(20)]
position_dirt_cat = [(randrange(0, NUM_ROWS, 1), randrange(0, NUM_COLS, 1)) for _ in range(20)]

for x, y in position_dirt_dust:
    GRID.add_object((y, x), '1')
    GRID.add_weight((y, x), 20)

for x, y in position_dirt_water:
    GRID.add_object((y, x), '2')
    GRID.add_weight((y, x), 5)

for x, y in position_dirt_cat:
    GRID.add_object((y, x), '3')
    GRID.add_weight((y, x), 10)

draw_grid(GRID)


point_start = tuple(position_cleaner)
point_goal = (0, 8)
came_from, cost_so_far = a_star_search(GRID, point_start, point_goal)
reconstruction = reconstruct_path(came_from, start=point_start, goal=point_goal)


play = True
show_path = False

# -------- Main Program Loop -----------
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if position_cleaner[0] > 0:
                    position_cleaner[0] -= CELL_WIDTH
            if event.key == pygame.K_RIGHT:
                if position_cleaner[0] < CELL_WIDTH * (NUM_COLS - 1):
                    position_cleaner[0] += CELL_WIDTH
            if event.key == pygame.K_UP:
                if position_cleaner[1] > 0:
                    position_cleaner[1] -= CELL_HEIGHT
            if event.key == pygame.K_DOWN:
                if position_cleaner[1] < CELL_HEIGHT * (NUM_ROWS - 1):
                    position_cleaner[1] += CELL_HEIGHT

            if event.key == pygame.K_END:
                show_path = True
                for x, y in reconstruction:
                    screen.blit(cleaner_image, (x * CELL_WIDTH, y * CELL_HEIGHT))
                    pygame.display.flip()
                    pygame.time.wait(100)

            if event.key == pygame.K_1:
                position_cleaner = [0, 0]
                point_goal = (0, 8)
                point_start = tuple(position_cleaner)
                came_from, cost_so_far = a_star_search(GRID, point_start, point_goal)
                reconstruction = reconstruct_path(came_from, start=point_start, goal=point_goal)

                print()
                print("PATH FROM POINT {} to {}".format(point_start, point_goal))
                draw_grid(GRID, path=reconstruction)

            if event.key == pygame.K_2:
                position_cleaner = [11, 8]
                point_goal = (11, 13)
                point_start = tuple(position_cleaner)
                came_from, cost_so_far = a_star_search(GRID, point_start, point_goal)
                reconstruction = reconstruct_path(came_from, start=point_start, goal=point_goal)

                print()
                print("PATH FROM POINT {} to {}".format(point_start, point_goal))
                draw_grid(GRID, path=reconstruction)

            if event.key == pygame.K_3:
                position_cleaner = [0, 0]
                point_goal = (11, 13)
                point_start = tuple(position_cleaner)
                came_from, cost_so_far = a_star_search(GRID, point_start, point_goal)
                reconstruction = reconstruct_path(came_from, start=point_start, goal=point_goal)

                print()
                print("PATH FROM POINT {} to {}".format(point_start, point_goal))
                draw_grid(GRID, path=reconstruction)

    show_path = False

    # Set the screen background
    screen.fill(GREY)

    # Draw the grid
    for row in range(NUM_ROWS):
        for column in range(NUM_COLS):
            screen.blit(cell_image, [column * CELL_WIDTH, row * CELL_HEIGHT])

    for row in range(NUM_ROWS):
        for column in range(NUM_COLS):
            item = GRID.objects.get((column, row), "")
            if item == '1':
                screen.blit(dirt_dust_image, [column * CELL_WIDTH, row * CELL_HEIGHT])
            elif item == '2':
                screen.blit(dirt_water_image, [column * CELL_WIDTH, row * CELL_HEIGHT])
            elif item == '3':
                screen.blit(dirt_cat_image, [column * CELL_WIDTH, row * CELL_HEIGHT])

    for furniture in GRID.furnitures:
        screen.blit(furniture.image, furniture.position)

    if not show_path:
        screen.blit(cleaner_image, (position_cleaner[0] * CELL_WIDTH, position_cleaner[1] * CELL_HEIGHT))

    pygame.draw.circle(screen, BLACK, (point_goal[0] * CELL_WIDTH + 15, point_goal[1] * CELL_HEIGHT + 15), 15)
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
