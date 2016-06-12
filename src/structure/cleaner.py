import cv2
import pygame

from object import Object
from src.core.algorithm import a_star_search, reconstruct_path, path_as_orders
from src.core.neuron import NeuralTest
from src.extra.draw import draw_grid
from src.extra.settings import WIDTH, HEIGHT


class Cleaner(Object):
    def __init__(self, name, position, texture):
        super(Cleaner, self).__init__(name, position)
        self.image = pygame.image.load(texture).convert_alpha()
        self.battery = 100
        self.soap = 100
        self.container = 100
        self.data = dict()
        self.obj_images = dict()  # paths of images (for neural network)
        self.board = None
        self.screen = None
        self.network = None
        self.classification = None
        self.clean_all = False

    def assign_board(self, board):
        """Assign the board, on which the agent will be doing tasks (move, clean etc.)."""
        self.board = board

    def assign_screen(self, screen):
        """Assign the screen, on which the agent is going to be displayed."""
        self.screen = screen

    def assign_network(self, network):
        """Assign previously created neural network for image recognition."""
        self.network = network

    def assign_classification(self, classification):
        """Assign previously created classification (which creates decision tree) for decision making."""
        self.classification = classification

    def assign_images(self, images):
        """Assign path of images. This is necessary for image recognition (algorithm loads image using path)."""
        self.obj_images = images

    def set_cleaning(self):
        """Informs agent to clean all objects on board. Changes clean_all flag to True."""
        if self.board.dirt and not self.data:
            print("\nNO INFORMATION ABOUT DIRT, PLEASE LAUNCH RECOGNITION PROCESS.")
        elif not self.board.dirt:
            print("\nCLEAN AS A WHISTLE, SIR!")
        elif self.clean_all:
            print("\nCLEANING STOPPED")
            self.clean_all = False
        else:
            print("\nCLEANING...")
            self.clean_all = True

    def move(self, vector):
        """Shift the position of the object on the board by vector (x (horizontally) and y (vertically))."""
        destination = (self.position[0] + vector[0], self.position[1] + vector[1])
        if self.board.passable(destination) and self.board.in_bounds(destination):
            self.position = destination

    def find_closest(self):
        """Find position of dirt, which is closest from current position of the agent.

        The distance is "Manhattan distance" (strictly horizontal and/or vertical path).
        """
        closest = WIDTH * HEIGHT  # maximum possible distance on the board
        closest_pos = self.board.station.position
        for item in self.data.keys():
            distance = abs(self.position[0] - item[0]) + abs(self.position[1] - item[1])
            if distance < closest:
                closest = distance
                closest_pos = item
        return closest_pos

    def go_to_station(self):
        """Move agent from it's current position to the position of the docking station."""
        self.move_to(self.board.station.position, static_board=False)

    def refresh(self):
        """Refill agent's properties."""
        self.battery = 100
        self.soap = 100
        self.capacity = 100

    def recognize(self, position=("", )):
        """Using assigned neural network, recognize object by image at current position."""
        if isinstance(position[0], str):  # check if optional parameter was provided
            position = self.position

        recognition = ""
        image = self.obj_images.get(self.board.get_object_name(position), "")

        if image:
            test = NeuralTest(cv2.imread(image))
            test.prepare_test_data()
            recognition = self.network.test_network(test)
            print("{} is {}".format(position, recognition))

        if recognition:
            self.data[position] = recognition

    def collect_data(self):
        """Using assigned neural network, recognize all images on the screen and save it if the object is dirt."""
        self.data = dict()
        print("\nCOLLECTING DATA...")

        for y in range(self.board.height):
            for x in range(self.board.width):
                self.recognize((x, y))

        if not self.data:
            print("\nSORRY, THERE IS NOTHING TO CLEAN.")
        else:
            print("\nCOLLECTED INFORMATION ABOUT DIRT.")

    def move_to(self, point_goal, static_board=True, draw=True):
        """Move agent from it's current position to point_goal.

        Path to destination point is created using A* algorithm.

        Parameters:
        - static_board - draw agent on new position, but leave previous positions on screen
        - draw - print current game board with path in console
        """
        came_from, cost_so_far = a_star_search(self.board, self.position, point_goal, 'up')
        reconstruction = reconstruct_path(came_from, start=self.position, goal=point_goal)

        if draw:
            print("\nPATH FROM POINT {} to {}".format(self.position, point_goal))
            draw_grid(self.board, path=reconstruction, start=self.position, goal=point_goal)

            print("\nORDERS FOR AGENT TO MOVE")
            print(", ".join(path_as_orders(reconstruction)))

        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # [up, right, down, left] - clockwise
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
                self.move(directions[direction])

            if not static_board:
                self.board.draw()  # update screen (removes images that are not actual)

            self.screen.blit(self.image, self.screen_position())
            pygame.time.Clock().tick(60)  # frames per second
            pygame.display.update()
            pygame.time.wait(20)  # milliseconds pause before next step

        self.image = pygame.transform.rotate(self.image, -rotation)

    def clean(self):
        """Remove object (dirt) from board at current position."""
        if self.position in self.data.keys():
            self.board.clean_object(self.position)
            del self.data[self.position]

    def clean_next(self):
        """Find closest object, move to it and clean it. Provide proper information in console"""
        if self.data:
            destination = self.find_closest()
            self.board.point_goal = destination
            self.move_to(destination, False, False)
            self.clean()
        elif not self.board.dirt:  # if agent collected all the information and cleaned all dirt from the board
            print("\nCLEANING COMPLETED.")
            self.clean_all = False
        else:  # there is still some dirt on the board, but the agent didn't collect information about it
            print("\nNO INFORMATION ABOUT DIRT.")

    def draw(self):
        """Draw agent image on previously assigned screen."""
        if self.clean_all:
            self.clean_next()
        self.screen.blit(self.image, self.screen_position())

    def generate_and_clean(self, amount):
        """Generates new random dirt on board and automatically sets agent to clean all."""
        if not self.board.dirt:
            self.board.generate_random_dirt(amount)
            self.board.draw()
            self.draw()
            pygame.display.update()
            # agent.set_position((0, 0))
        self.collect_data()
        self.set_cleaning()

    def make_decision(self):
        pass
