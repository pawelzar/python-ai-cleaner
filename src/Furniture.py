class Furniture(object):
    width = 0
    length = 0
    height_from_floor = 0
    position = ()

    def __init__(self, x, y, width, length, height):
        self.position = (x, y)
        self.width = width
        self.length = length
        self.height_from_floor = height

    def set_position(self, x, y):
        self.super.x = x
        self.super.y = y
