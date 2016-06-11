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
        self.clean_all = False

    def set_position(self, x, y):
        """Set the position of the object on the board."""
        self.position = (x, y)

    def assign_board(self, board):
        """Assign the board, on which the agent will be doing tasks (move, clean etc.)."""
        self.board = board

    def assign_screen(self, screen):
        """Assign the screen, on which the agent is going to be displayed."""
        self.screen = screen

    def assign_network(self, network):
        """Assign previously created neural network for image recognition."""
        self.network = network

    def move(self, x, y):
        """Shift the position of the object on the board by vector (x (horizontally) and y (vertically))."""
        self.position = (self.position[0] + x, self.position[1] + y)

    def find_closest(self):
        """Find position of dirt, which is closest from current position of the agent.

        The distance is "Manhattan distance" (strictly horizontal and/or vertical path).
        """
        closest = NUM_ROWS * NUM_COLS
        closest_pos = self.board.station.position
        for item in self.data.keys():
            distance = abs(self.position[0] - item[0]) + abs(self.position[1] - item[1])
            if distance < closest:
                closest = distance
                closest_pos = item
        return closest_pos

    def go_to_station(self):
        """Move agent from it's current position to the position of the docking station."""
        self.move_to(self.board.station.position)

    def refresh(self):
        """Refill agent's properties."""
        self.battery = 100
        self.soap = 100
        self.capacity = 100

    def clean(self):
        """Remove object (dirt) from board at current position."""
        if self.position in self.data.keys():
            self.board.clean_object(self.position)
            del self.data[self.position]

    def recognize(self, images, position=("", )):
        """Using assigned neural network, recognize object by image at current position."""
        if isinstance(position[0], str):
            position = self.position

        recognition = ""
        image = images.get(self.board.get_object_name(position), "")

        if image:
            test = NeuralTest(cv2.imread(image))
            test.prepare_test_data()
            recognition = self.network.test_network(test)
            print("{} is {}".format(position, recognition))

        return recognition

    def collect_data(self, images):
        """Using assigned neural network, recognize all images on the screen and save it if the object is dirt."""
        self.data = dict()
        print("\nCOLLECTING DATA...")

        for y in range(self.board.height):
            for x in range(self.board.width):
                recognition = self.recognize(images, (x, y))
                if recognition:
                    self.data[(x, y)] = recognition

        if not self.data:
            print("\nSORRY, THERE IS NOTHING TO CLEAN.")
        else:
            print("\nCOLLECTED INFORMATION ABOUT DIRT.")

    def move_to(self, point_goal, static_board=True, draw=True):
        """Move agent from it's current position to position_goal.

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

            if not static_board:
                self.board.draw()

            self.screen.blit(self.image, self.screen_position())
            pygame.time.Clock().tick(60)
            pygame.display.update()
            pygame.time.wait(20)

        self.image = pygame.transform.rotate(self.image, -rotation)

    def clean_all(self):
        """Remove all objects (dirt) from board."""
        if self.board.dirt and not self.data:
            print("\nNO INFORMATION ABOUT DIRT, PLEASE LAUNCH RECOGNITION PROCESS.")
        else:
            print("\nCLEANING...")

            #while self.data:
            #    point_goal = self.find_closest()
            #    self.move_to(point_goal, False, False)
            #    self.clean()

            for pos in sorted(self.data.keys()):
                #print pos
                self.move_to(pos, False, False)
                self.clean()

            print("\nCLEAN AS A WHISTLE, SIR!")

    def draw(self):
        """Draw agent image on previously assigned screen."""
        self.screen.blit(self.image, self.screen_position())


    def wtf(self, clock):
        i = 1
        val = 0
        while True:
            i+=1
            x=[(1,0), (-1,0)]
            self.move(*x[val])
            if i % NUM_COLS == 0:
                i = 1
                val = not val
            self.board.draw()
            self.screen.blit(self.image, self.screen_position())
            pygame.time.wait(0)
            clock.tick(60)
            pygame.display.update()

    def set_to_cleaning(self):
        self.clean_all = True

    def clean_2(self):
        if self.clean_all and self.data:
            self.move_to(self.find_closest(), False, False)
            self.clean()
        else:
            self.clean_all = False

    def make_decision(self):
        pass
