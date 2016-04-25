import pygame

from src.draw import draw_grid
from src.graph import SquareGrid
from src.screen_settings import *
from random import randrange


# Initialize board
GRID = SquareGrid(NUM_COLS, NUM_ROWS)

# Initialize display
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("PRO CLEANER 9000")
clock = pygame.time.Clock()

# Load images
cell_image = pygame.image.load("../images/floor_cell.jpg").convert_alpha()
cleaner_image = pygame.image.load("../images/cleaner.png").convert_alpha()
cleaner_image.set_colorkey(BLACK)

dirt_dust_image = pygame.image.load("../images/dirt_dust.png").convert_alpha()
dirt_dust_image.set_colorkey(BLACK)
dirt_water_image = pygame.image.load("../images/dirt_water.png").convert_alpha()
dirt_water_image.set_colorkey(BLACK)
dirt_cat_image = pygame.image.load("../images/dirt_cat.png").convert_alpha()
dirt_cat_image.set_colorkey(BLACK)

furniture_chair_image = pygame.image.load("../images/furniture_chair.png").convert_alpha()
furniture_chair_image.set_colorkey(BLACK)
furniture_sofa_image = pygame.image.load("../images/furniture_sofa.png").convert_alpha()
furniture_sofa_image.set_colorkey(BLACK)

position_chair = [60, 90]
position_sofa = [300, 300]

background_position = [0, 0]
cleaner_x = 210
cleaner_y = 210
print(furniture_chair_image.get_rect())
print(furniture_sofa_image.get_rect())


position_dirt_dust = [(randrange(0, NUM_ROWS, 1), randrange(0, NUM_COLS, 1)) for _ in range(20)]
position_dirt_water = [(randrange(0, NUM_ROWS, 1), randrange(0, NUM_COLS, 1)) for _ in range(20)]
position_dirt_cat = [(randrange(0, NUM_ROWS, 1), randrange(0, NUM_COLS, 1)) for _ in range(20)]

for x, y in position_dirt_dust:
    GRID.add_object((x, y), '1')

for x, y in position_dirt_water:
    GRID.add_object((x, y), '2')

for x, y in position_dirt_cat:
    GRID.add_object((x, y), '3')

draw_grid(GRID)


play = True

# -------- Main Program Loop -----------
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if cleaner_x > 0:
                    cleaner_x -= CELL_WIDTH
            if event.key == pygame.K_RIGHT:
                if cleaner_x < CELL_WIDTH * (NUM_COLS - 1):
                    cleaner_x += CELL_WIDTH
            if event.key == pygame.K_UP:
                if cleaner_y > 0:
                    cleaner_y -= CELL_HEIGHT
            if event.key == pygame.K_DOWN:
                if cleaner_y < CELL_HEIGHT * (NUM_ROWS - 1):
                    cleaner_y += CELL_HEIGHT

    # Set the screen background
    screen.fill(GREY)

    # Draw the grid
    for row in range(NUM_ROWS):
        for column in range(NUM_COLS):
            screen.blit(cell_image, [column * CELL_WIDTH, row * CELL_HEIGHT])

    for row in range(NUM_ROWS):
        for column in range(NUM_COLS):
            item = GRID.objects.get((row, column), "")
            if item == '1':  # grid[row][column] == 1:
                screen.blit(dirt_dust_image, [column * CELL_WIDTH, row * CELL_HEIGHT])
            elif item == '2':  # grid[row][column] == 2:
                screen.blit(dirt_water_image, [column * CELL_WIDTH, row * CELL_HEIGHT])
            elif item == '2':  # grid[row][column] == 3:
                screen.blit(dirt_cat_image, [column * CELL_WIDTH, row * CELL_HEIGHT])

    screen.blit(furniture_chair_image, position_chair)
    screen.blit(furniture_sofa_image, position_sofa)
    screen.blit(cleaner_image, [cleaner_x, cleaner_y])
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
