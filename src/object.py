from src.screen_settings import *


class Object:
    def __init__(self, name, position, size=(CELL_WIDTH, CELL_HEIGHT)):
        self.name = name
        self.position = position
        self.size = size

    def pos_x(self):
        return self.position[0]

    def pos_y(self):
        return self.position[1]

    def get_width(self):
        return self.size[0] // CELL_WIDTH

    def get_height(self):
        return self.size[1] // CELL_HEIGHT

    def real_position(self):
        return self.position[0] * CELL_WIDTH, self.position[1] * CELL_HEIGHT

    def set_position(self, x, y):
        self.position = (x, y)

    def move(self, x, y):
        self.position = (self.position[0] + x, self.position[1] + y)
