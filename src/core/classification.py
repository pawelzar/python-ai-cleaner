from core.dtree import create_decision_tree, get_classification
from core.id3 import gain
from extra.draw import draw_tree as draw


class Classification:
    def __init__(self, train_cleaning, train_refill):
        self.tree_clean = self.create_tree(train_cleaning)
        self.tree_refill = self.create_tree(train_refill)

    @staticmethod
    def create_tree(training_set):
        """
        Load file with training set and create decision tree
        based on acquired data.
        """
        defined = open(training_set, 'r')
        lines = defined.readlines()
        defined.close()

        attributes = lines.pop(0).split()  # first row is for values names
        target_attr = attributes[-1]  # last column is for the result
        values = [line.split() for line in lines]  # all examples from the set

        # create list of dictionaries
        # (each dictionary consists of names of attributes and proper values)
        # e.g. {'DISTANCE': 'close', 'TYPE': 'dust', 'SOAP': 'low', ...}
        data = [dict(zip(attributes, current)) for current in values]

        return create_decision_tree(data, attributes, target_attr, gain)

    def classify(self, distance, instance, soap, battery, container):
        """
        Return decision to clean the object or not.
        """
        collection = dict()
        collection['DISTANCE'] = distance
        collection['TYPE'] = instance
        collection['SOAP'] = soap
        collection['BATTERY'] = battery
        collection['CONTAINER'] = container
        return get_classification(self.tree_clean, collection)

    def classify_refill(self, dist_sta, dist_bin, battery, soap, container):
        """
        Return decision where the agent should go
        (e.g. if battery is low or container is empty).
        """
        collection = dict()
        collection['DIST_STA'] = dist_sta
        collection['DIST_BIN'] = dist_bin
        collection['BATTERY'] = soap
        collection['SOAP'] = battery
        collection['CONTAINER'] = container
        return get_classification(self.tree_refill, collection)

    def draw_cleaning_tree(self):
        print '\nDECISION TREE (CLEANING)'
        draw(self.tree_clean)

    def draw_refill_tree(self):
        print '\nDECISION TREE (REFILL)'
        draw(self.tree_refill)
