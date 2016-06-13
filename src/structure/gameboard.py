from random import randrange

import pygame

from graph import GridWithWeights
from object import Object
from src.extra.draw import draw_grid
from src.extra.settings import *


class GameBoard(GridWithWeights):
    def __init__(self, width, height):
        super(GameBoard, self).__init__(width, height)
        self.furniture = []
        self.dirt = []
        self.agent = None
        self.screen = None
        self.images = None
        self.station = None
        self.basket = None
        self.point_goal = None

    def add_furniture(self, furniture):
        """Add object to the board that the agent can not pass through."""
        self.furniture.append(furniture)
        for row in range(furniture.get_width()):
            for column in range(furniture.get_height()):
                self.add_obstacle((furniture.pos_x() + row, furniture.pos_y() + column))

    def add_dirt(self, dirt):
        """Add dirt object to the board."""
        self.dirt.append(dirt)

    def add_station(self, station):
        """Assign station to the board."""
        self.station = station

    def add_bin(self, basket):
        """Assign trash can to the board."""
        self.basket = basket

    def assign_agent(self, agent):
        """Assign agent to the board. This is necessary for printing board in console."""
        self.agent = agent

    def get_object_name(self, position):
        """Return name of the object placed at given position."""
        for item in self.dirt:
            if item.position == position:
                return item.name

    def get_points(self):
        """Return all points, at which there are some objects (dirt or furniture)."""
        return self.obstacles.keys() + [item.position for item in self.dirt + [self.station, self.basket]]

    def get_furniture_points(self):
        """Return sorted list of furniture positions.

        The dictionary of obstacles represents positions that are locked and agent cannot move through them.
        Thus it represents positions of the furniture on the board.
        """
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

    def clean_all_dirt(self):
        """Remove all dirt from the board, including weights."""
        for i, item in enumerate(self.dirt):
            del self.objects[item.position]
            del self.weights[item.position]
        self.dirt = []

    def generate_random(self, name, character, weight, amount):
        """Add as many objects of type dirt to the board as the amount specified.

        Each position is generated randomly and is unique.
        Position values are limited by the size of the board.

        Parameters:
        - name - all objects generated here will have this name
        - character - all objects generated here be represented by this character (e.g. when printing board in console)
        - weight - this will have influence on creating path by an algorithm (A*)
        - amount - number of objects to be generated
        """
        for i in range(amount):
            (x, y) = (randrange(0, self.width, 1), randrange(0, self.height, 1))
            while (x, y) in self.get_points():
                (x, y) = (randrange(0, self.width, 1), randrange(0, self.height, 1))

            self.add_object((x, y), character)
            self.add_weight((x, y), weight)
            self.add_dirt(Object(name, (x, y)))

    def generate_random_dirt(self, amount):
        """Fill board with dirt placed on random positions. Also assign proper weights and signs."""
        self.clean_all_dirt()
        self.generate_random("dust", "1", 20, amount)
        self.generate_random("water", "2", 5, amount)
        self.generate_random("cat", "3", 10, amount)

    def draw(self):
        """Draw board images on previously assigned screen."""
        # Set the screen background
        self.screen.fill(GREY)

        # Draw the grid
        for row in range(HEIGHT):
            for column in range(WIDTH):
                self.screen.blit(self.images["floor"],
                                 [column * CELL_WIDTH + (CELL_MARGIN / 2), row * CELL_HEIGHT + (CELL_MARGIN / 2)])

        # Draw board elements
        for dirt in self.dirt:
            self.screen.blit(self.images[dirt.name], dirt.screen_position())

        for furniture in self.furniture + [self.station, self.basket]:
            self.screen.blit(self.images[furniture.name], furniture.screen_position())

        # Draw crossed lines at point goal
        self.draw_target(self.point_goal)

    def draw_target(self, point_goal):
        """Draw crossed lines at the target point on screen."""
        pygame.draw.line(self.screen, GREY, ((point_goal[0] + 0.5) * CELL_WIDTH - 1, point_goal[1] * CELL_HEIGHT),
                         ((point_goal[0] + 0.5) * CELL_WIDTH - 1, (point_goal[1] + 1) * CELL_HEIGHT - 1), 4)
        pygame.draw.line(self.screen, GREY, (point_goal[0] * CELL_WIDTH, (point_goal[1] + 0.5) * CELL_HEIGHT - 1),
                         ((point_goal[0] + 1) * CELL_WIDTH - 1, (point_goal[1] + 0.5) * CELL_HEIGHT - 1), 4)

    def print_in_console(self):
        """Print nice looking grid in console."""
        print("\nCURRENT GAME BOARD")
        draw_grid(self)
