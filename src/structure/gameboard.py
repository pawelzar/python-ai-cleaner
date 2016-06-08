from random import randrange

import pygame

from graph import GridWithWeights
from object import Object
from src.settings import *


class GameBoard(GridWithWeights):
    def __init__(self, width, height):
        super(GameBoard, self).__init__(width, height)
        self.furniture = []
        self.dirt = []
        self.agent = None
        self.screen = None
        self.images = None
        self.station = None

    def add_furniture(self, furniture):
        """Add object to the board that the agent can not pass through."""
        self.furniture.append(furniture)
        for row in range(furniture.get_width()):
            for column in range(furniture.get_height()):
                self.add_obstacle((furniture.pos_x() + row, furniture.pos_y() + column))

    def add_dirt(self, dirt):
        """Add dirt object to the board."""
        self.dirt.append(dirt)

    def add_agent(self, agent):
        """Assign agent to the board."""
        self.agent = agent

    def add_station(self, station):
        """Assign agent to the board."""
        self.station = station

    def get_object_name(self, position):
        """Return name of the object placed at given position."""
        for item in self.dirt:
            if item.position == position:
                return item.name

    def get_points(self):
        """Return all points, at which there are some objects (dirt or furniture)."""
        return self.obstacles.keys() + [item.position for item in self.dirt]

    def get_furniture_points(self):
        """Return list of furniture positions."""
        return sorted(self.obstacles.keys())

    def get_dirt_points(self):
        """Return list of dirt positions."""
        return [item.position for item in self.dirt]

    def assign_screen(self, screen):
        """Assign the screen, on which the elements of the board are going to be displayed."""
        self.screen = screen

    def assign_images(self, images):
        """Assign images to the board."""
        self.images = images

    def clean_object(self, position):
        """Remove object at given position from board, including weight."""
        for i, item in enumerate(self.dirt):
            if item.position == position:
                del self.dirt[i]
                del self.objects[position]
                del self.weights[position]

    def generate_random_dirt(self, amount):
        """Fill board with dirt placed on random positions. Also assign proper weights and sign."""
        for i in range(amount):
            (x, y) = (randrange(0, NUM_COLS, 1), randrange(0, NUM_ROWS, 1))
            while (x, y) in self.get_points():
                (x, y) = (randrange(0, NUM_COLS, 1), randrange(0, NUM_ROWS, 1))

            self.add_object((x, y), '1')
            self.add_weight((x, y), 20)
            self.add_dirt(Object("dust", (x, y)))

        for i in range(amount):
            (x, y) = (randrange(0, NUM_COLS, 1), randrange(0, NUM_ROWS, 1))
            while (x, y) in self.get_points():
                (x, y) = (randrange(0, NUM_COLS, 1), randrange(0, NUM_ROWS, 1))

            self.add_object((x, y), '2')
            self.add_weight((x, y), 5)
            self.add_dirt(Object("water", (x, y)))

        for i in range(amount):
            (x, y) = (randrange(0, NUM_COLS, 1), randrange(0, NUM_ROWS, 1))
            while (x, y) in self.get_points():
                (x, y) = (randrange(0, NUM_COLS, 1), randrange(0, NUM_ROWS, 1))

            self.add_object((x, y), '3')
            self.add_weight((x, y), 10)
            self.add_dirt(Object("cat", (x, y)))

    def draw(self):
        """Draw board images on previously assigned screen."""
        # Set the screen background
        self.screen.fill(GREY)

        # Draw the grid
        for row in range(NUM_ROWS):
            for column in range(NUM_COLS):
                self.screen.blit(self.images["floor"], [column * CELL_WIDTH + (CELL_MARGIN / 2),
                                                        row * CELL_HEIGHT + (CELL_MARGIN / 2)])

        # Draw board elements
        for dirt in self.dirt:
            self.screen.blit(self.images[dirt.name], dirt.screen_position())

        for furniture in self.furniture + [self.station]:
            self.screen.blit(self.images[furniture.name], furniture.screen_position())

    def draw_target(self, point_goal):
        """Draw crossed lines at the target point on screen."""
        pygame.draw.line(self.screen, GREY, ((point_goal[0] + 0.5) * CELL_WIDTH - 1, point_goal[1] * CELL_HEIGHT),
                         ((point_goal[0] + 0.5) * CELL_WIDTH - 1, (point_goal[1] + 1) * CELL_HEIGHT - 1), 4)
        pygame.draw.line(self.screen, GREY, (point_goal[0] * CELL_WIDTH, (point_goal[1] + 0.5) * CELL_HEIGHT - 1),
                         ((point_goal[0] + 1) * CELL_WIDTH - 1, (point_goal[1] + 0.5) * CELL_HEIGHT - 1), 4)
