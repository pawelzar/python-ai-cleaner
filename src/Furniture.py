import pygame


class Furniture:
    def __init__(self, pos_x, pos_y, image_path):
        self.position = (pos_x, pos_y)
        self.name = image_path
        self.image = pygame.image.load(image_path).convert_alpha()

    def __string__(self):
        return self.name

    def set_position(self, pos_x, pos_y):
        self.position = (pos_x, pos_y)

    def get_position(self):
        return self.position

    def get_image(self):
        return self.image
