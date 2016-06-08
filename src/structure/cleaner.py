import cv2
import pygame

from object import Object

from src.draw import draw_grid
from src.neuron import NeuralTest
from src.settings import NUM_COLS, NUM_ROWS
from src.algorithm import a_star_search, reconstruct_path, path_as_orders


class Cleaner(Object):
    def __init__(self, name, position):
        super(Cleaner, self).__init__(name, position)
        self.image = pygame.image.load("../images/cleaner.png").convert_alpha()
        self.battery = 100
        self.soap = 100
        self.capacity = 100
        self.data = dict()
        self.board = None
        self.screen = None
        self.network = None

    def set_position(self, x, y):
        """Set the position of the object on the board."""
        self.position = (x, y)

    def move(self, x, y):
        """Shift the position of the object on the board by vector (x (horizontally) and y (vertically))."""
        self.position = (self.position[0] + x, self.position[1] + y)

    def find_closest(self):
        closest = NUM_ROWS * NUM_COLS
        closest_pos = (0, 0)
        for item in self.board.dirt:
            distance = abs(self.position[0] - item.position[0]) + abs(self.position[1] - item.position[1])
            if distance < closest:
                closest = distance
                closest_pos = item.position
        return closest_pos

    def assign_board(self, board):
        self.board = board

    def assign_screen(self, screen):
        self.screen = screen

    def assign_network(self, network):
        self.network = network

    def go_to_station(self):
        self.move_to(self.board.station.position)

    def refresh(self):
        self.battery = 100
        self.soap = 100
        self.capacity = 100

    def collect_data(self, images):
        self.data = dict()
        print("\nCOLLECTING DATA...")
        for y in range(self.board.height):
            for x in range(self.board.width):
                image = images.get(self.board.get_object_name((x, y)), "")
                if image:
                    test = NeuralTest(cv2.imread(image))
                    test.prepare_test_data()
                    recognition = self.network.test_network(test)
                    print "({}, {}) is {}".format(x, y, recognition)
                    self.data[(x, y)] = recognition

    def clean(self):
        self.board.clean_object(self.position)

    def move_to(self, point_goal):
        came_from, cost_so_far = a_star_search(self.board, self.position, point_goal, 'up')
        reconstruction = reconstruct_path(came_from, start=self.position, goal=point_goal)

        print("\nPATH FROM POINT {} to {}".format(self.position, point_goal))
        draw_grid(self.board, path=reconstruction, start=self.position, goal=point_goal)

        print("\nORDERS FOR AGENT TO MOVE")
        print(", ".join(str(x) for x in path_as_orders(reconstruction)))

        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # [up, right, down, left]
        direction = 0
        rotation = 0
        for order in path_as_orders(reconstruction):
            if order == 'turn right':
                rotation -= 90
                self.image = pygame.transform.rotate(self.image, -90)
                direction = (direction + 1) % 4
            elif order == 'turn left':
                rotation += 90
                self.image = pygame.transform.rotate(self.image, 90)
                direction = (direction - 1) % 4
            else:
                self.move(*directions[direction])

            self.screen.blit(self.image, self.real_position())
            pygame.display.flip()
            pygame.time.wait(50)

        self.image = pygame.transform.rotate(self.image, -rotation)

    def clean_all(self):
        print("\nCLEANING...")
        while self.board.dirt:
            point_goal = self.find_closest()
            came_from, cost_so_far = a_star_search(self.board, self.position, point_goal, 'up')
            reconstruction = reconstruct_path(came_from, start=self.position, goal=point_goal)

            directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # [up, right, down, left]
            direction = 0
            rotation = 0
            for order in path_as_orders(reconstruction):
                if order == 'turn right':
                    rotation -= 90
                    self.image = pygame.transform.rotate(self.image, -90)
                    direction = (direction + 1) % 4
                elif order == 'turn left':
                    rotation += 90
                    self.image = pygame.transform.rotate(self.image, 90)
                    direction = (direction - 1) % 4
                else:
                    self.move(*directions[direction])

                # screen.blit(images["agent"], agent.real_position())
                self.board.draw()
                self.screen.blit(self.image, self.real_position())
                # clock.tick(60)
                pygame.display.flip()
                pygame.time.wait(50)

            self.board.clean_object(self.position)
            self.image = pygame.transform.rotate(self.image, -rotation)

        print("\nCLEAN AS A WHISTLE, SIR!")

    def draw(self):
        self.screen.blit(self.image, self.real_position())