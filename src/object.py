from src.screen_settings import *


class Object:
    def __init__(self, name, position, size=(CELL_WIDTH, CELL_HEIGHT)):
        self.name = name
        self.position = position
        self.size = size

    def pos_x(self):
        """Return horizontal position on the board."""
        return self.position[0]

    def pos_y(self):
        """Return vertical position on the board."""
        return self.position[1]

    def get_width(self):
        """Return number of cells occupied horizontally by the object on the board."""
        return self.size[0] // CELL_WIDTH

    def get_height(self):
        """Return number of cells occupied vertically by the object on the board."""
        return self.size[1] // CELL_HEIGHT

    def real_position(self):
        """Return exact position in pixels on the screen."""
        return self.position[0] * CELL_WIDTH, self.position[1] * CELL_HEIGHT

    def set_position(self, x, y):
        """Set the position of the object on the board."""
        self.position = (x, y)

    def move(self, x, y):
        """Shift the position of the object on the board by vector (x (horizontally) and y (vertically))."""
        self.position = (self.position[0] + x, self.position[1] + y)
