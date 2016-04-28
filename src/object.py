from src.screen_settings import *


class Object:
    def __init__(self, name, position, size=(CELL_WIDTH, CELL_HEIGHT)):
        self.name = name
        self.position = position
        self.pos_x = position[0]
        self.pos_y = position[1]
        self.size = size

    def set_position(self, pos_x, pos_y):
        self.position = (pos_x, pos_y)

    def real_position(self):
        return self.position[0] * CELL_WIDTH, self.position[1] * CELL_HEIGHT

    def get_x(self):
        return self.pos_x

    def get_y(self):
        return self.pos_y

    def get_width(self):
        return self.size[0] // CELL_WIDTH

    def get_height(self):
        return self.size[1] // CELL_HEIGHT
