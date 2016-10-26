import cv2
import pygame

from object import Object
from src.core.algorithm import a_star_search, heuristic, path_as_orders
from src.core.neuron import Neuron
from src.extra.draw import draw_grid
from src.extra.settings import *
from src.extra.fuzzy import *
from src.genetic.optimize import optimize_route


class Cleaner(Object):
    def __init__(self, name, position, texture):
        super(Cleaner, self).__init__(name, position)
        self.image = pygame.image.load(texture).convert_alpha()
        self.battery = MAX_BATTERY
        self.soap = MAX_SOAP
        self.container = 0
        self.data = dict()
        self.obj_images = dict()  # paths of images (for neural network)
        self.board = None
        self.screen = None
        self.network = None
        self.classification = None
        self.clean_all = False
        self.optimal_path = []  # needed only if genetic algorithm is used

    def assign_board(self, board):
        """Assign the board, on which the agent will be doing tasks
        (move, clean etc.)."""
        self.board = board

    def assign_screen(self, screen):
        """Assign the screen, on which the agent is going to be displayed."""
        self.screen = screen

    def assign_network(self, network):
        """Assign previously created neural network for image recognition."""
        self.network = network

    def assign_classification(self, classification):
        """Assign previously created classification
        (which creates decision tree) for decision making."""
        self.classification = classification

    def assign_images(self, images):
        """Assign path of images. This is necessary for image recognition
        (algorithm loads image using path to it)."""
        self.obj_images = images

    def set_cleaning(self):
        """Inform agent to clean all objects on board.
        Change clean_all flag to True if there is dirt and
        agent collected data, False otherwise.
        """
        if self.board.dirt and not self.data:
            print("\nNO INFORMATION ABOUT DIRT, LAUNCH RECOGNITION PROCESS.")
        elif not self.board.dirt:
            print("\nCLEAN AS A WHISTLE, SIR!")
        elif self.clean_all:
            print("\nCLEANING STOPPED")
            self.clean_all = False
        else:
            print("\nCLEANING...")
            self.clean_all = True

    def move(self, vector):
        """Shift the position of the object on the board by vector
        (x (horizontally) and y (vertically))."""
        dest = (self.position[0] + vector[0], self.position[1] + vector[1])
        if self.board.passable(dest) and self.board.in_bounds(dest):
            self.position = dest
            self.battery -= 0.5
            self.print_stats()

    def find_closest(self):
        """Find position of dirt, which is closest from
        current position of the agent, using "Manhattan distance"
        (strictly horizontal and/or vertical path).
        """
        closest = WIDTH * HEIGHT  # maximum possible distance on the board
        closest_pos = self.board.station.position
        for item in self.data.keys():
            distance = abs(self.position[0] - item[0]) + \
                       abs(self.position[1] - item[1])
            if distance < closest:
                closest = distance
                closest_pos = item
        return closest_pos

    def go_to_station(self):
        """Move agent from it's current position to the
        position of the docking station."""
        self.move_to(self.board.station.position, static_board=False)

    def go_to_bin(self):
        """Move agent from it's current position to the
        position of the trash can."""
        self.move_to(self.board.basket.position, static_board=False)

    def reload(self):
        """Reload agent's properties."""
        if self.position == self.board.station.position:
            print("\nAGENT RELOADED IN DOCKING STATION.")
            self.battery = MAX_BATTERY
            self.soap = MAX_SOAP
            # self.container = 0

    def empty_container(self):
        """Leave all dirt in trash can."""
        if self.position == self.board.basket.position:
            print("\nAGENT THREW DIRT TO RUBBISH BIN.")
            self.container = 0

    def recognize(self, position=("", )):
        """Using assigned neural network,
        recognize object by image at current position."""
        if isinstance(position[0], str):  # check if opt param was provided
            position = self.position

        recognition = ""
        image = self.obj_images.get(self.board.get_object_name(position), "")

        if image:
            test = Neuron(cv2.imread(image))
            test.prepare()
            recognition = self.network.test_network(test)
            print("{} is {}".format(position, recognition))

        if recognition:
            self.data[position] = recognition

    def collect_data(self):
        """Using assigned neural network, recognize all images
        on the screen and save it if the object is dirt."""
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
        - static_board - draw agent on new position, leave previous on screen
        - draw - print current game board with path in console
        """
        reconstruction = a_star_search(self.board, self.position, point_goal)
        self.board.point_goal = point_goal

        if draw:
            print("\nPATH FROM POINT {} to {}".
                  format(self.position, point_goal))

            draw_grid(self.board, path=reconstruction,
                      start=self.position, goal=point_goal)

            print("\nORDERS FOR AGENT TO MOVE")
            print(", ".join(path_as_orders(reconstruction)))

        # [up, right, down, left] - clockwise
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
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
                # update screen (removes images that are not actual)
                self.board.draw()

            self.screen.blit(self.image, self.screen_position())
            pygame.time.Clock().tick(60)  # frames per second
            pygame.display.update()
            pygame.time.wait(20)  # milliseconds pause before next step

        self.image = pygame.transform.rotate(self.image, -rotation)

    def clean(self):
        """Remove object (dirt) from board at current position."""
        if self.position in self.data.keys():
            self.board.clean_object(self.position)
            if self.data[self.position] == "cat":
                self.battery -= 4
                self.soap -= 9
                self.container += 8
            elif self.data[self.position] == "water":
                self.battery -= 2
                self.soap -= 7
                self.container += 5
            else:
                self.battery -= 3
                self.container += 7
            del self.data[self.position]

    def clean_next(self):
        """Find closest object, move to it and clean it.
        Provide proper information in console"""
        if self.data:
            destination = self.find_closest()
            self.move_to(destination, False, False)
            self.clean()
        elif not self.board.dirt:
            print("\nCLEANING COMPLETED.")  # if agent collected all the information and cleaned all dirt from the board
            self.clean_all = False
        else:  # there is still some dirt on the board, but the agent didn't collect information about it
            print("\nNO INFORMATION ABOUT DIRT.")
            self.clean_all = False

    def decide_to_clean(self, position, item):
        """Return result of classification using previously created tree
        (based on training set). Each attribute is changed into
        descriptive form, using fuzzy functions (to match the training set).
        The result is either True or False (to clean or not to clean).
        """
        instance = item  # name of the object (here type of the dirt)

        # gather information in descriptive form using fuzzy functions
        distance = fuzzy_distance(heuristic(self.position, position))
        soap = fuzzy_soap(self.soap)
        battery = fuzzy_battery(self.battery)
        container = fuzzy_container(self.container)

        result = self.classification.classify(distance, instance, soap,
                                              battery, container)
        print("distance: {}, type: {}, soap level: {}, "
              "battery: {}, container: {}, decision: {}".
              format(*map(str.upper, [distance, instance, soap,
                                      battery, container, result])))
        return result

    def decide_to_refill(self):
        """Return result of classification for moving cleaner to
        station or trash can. The result is either 'station' or 'bin'.
        This indicates where the cleaner should move.
        """
        dist_bin = fuzzy_distance(
            heuristic(self.position, self.board.basket.position))
        dist_sta = fuzzy_distance(
            heuristic(self.position, self.board.station.position))
        soap = fuzzy_soap(self.soap)
        battery = fuzzy_battery(self.battery)
        container = fuzzy_container(self.container)

        result = self.classification.classify_refill(
            dist_sta, dist_bin, battery, soap, container)

        print("distance to station: {}, distance to bin: {}, "
              "battery: {}, soap: {}, container: {}, decision: {}".
              format(*map(str.upper, [dist_sta, dist_bin, battery,
                                      soap, container, result])))
        return result

    def decide_and_clean(self):
        """Use decision tree to decide which action the agent should take.
        First iterate through each object and decide if cleaner can
        clean it in current state (battery level, etc.). If there is
        no object, which can be cleaned then cleaner returns
        to the station and reloads or removes trash to container.
        """
        if self.data:
            # items are sorted by distance from the cleaner
            # for position in self.optimal_path:
            closest = lambda x: heuristic(x[0], self.position)
            for position, item in sorted(self.data.items(), key=closest):
                # item = self.data[position]  # use if iterate through optimal path
                result = self.decide_to_clean(position, item)
                if result == "True":
                    self.move_to(position, False, False)
                    self.clean()
                    # self.optimal_path.remove(position)  # use if iterate through optimal path
                    break
            else:  # if cleaner is not able to clean any object (there was no break statement)
                refill = self.decide_to_refill()
                if refill == "station":
                    self.go_to_station()
                    self.reload()
                else:
                    self.go_to_bin()
                    self.empty_container()
                pygame.time.wait(200)

        elif not self.board.dirt:  # if agent collected all the information and cleaned all dirt from the board
            self.go_to_bin()
            self.empty_container()
            self.go_to_station()
            self.reload()
            print("\nCLEANING COMPLETED.")
            self.clean_all = False
        else:  # there is still some dirt on the board, but the agent didn't collect information about it
            print("\nNO INFORMATION ABOUT DIRT.")
            self.clean_all = False

    def draw(self):
        """Draw agent image on previously assigned screen."""
        if self.clean_all:
            # self.clean_next()  # without decision tree
            self.decide_and_clean()  # use decision tree to decide
            # self.print_stats()
        self.screen.blit(self.image, self.screen_position())

    def generate_and_clean(self, amount):
        """Generate new random dirt on board and
        automatically set agent to clean all."""
        if not self.board.dirt:
            self.board.generate_random_dirt(amount)
            self.board.draw()
            self.draw()
            pygame.display.update()
            # agent.set_position((0, 0))
        self.collect_data()
        # self.optimize_path()
        self.set_cleaning()

    def print_stats(self):
        """Print cleaner's current parameters in console."""
        print("battery: {}/150, soap: {}/100, container {}/100".
              format(self.battery, self.soap, self.container))

    def optimize_path(self):
        """Generate optimal path for clearing all dirt on the board."""
        self.optimal_path = \
            optimize_route(self.data.keys(), GENERATIONS, CROSSOVER_CHANCE,
                           MUTATION_CHANCE, POPULATION)
