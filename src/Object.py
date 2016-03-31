class Object(object):
    pos_x = 0
    pos_y = 0

    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def getPosition(self):
        return [self.pos_x, self.pos_y]
