from src.core.dtree import create_decision_tree, get_classification
from src.core.id3 import gain
from src.extra.draw import draw_tree as draw


class Classification:
    def __init__(self, train_cleaning, train_refill):
        defined = open(train_cleaning, "r")
        lines = defined.readlines()
        defined.close()

        attributes = lines.pop(0).split()  # first row represents the naming of values
        target_attr = attributes[-1]  # last column of training set represents the result
        values = [line.split() for line in lines]

        # create list of dictionaries (each dictionary consists of names of attributes and corresponding values)
        # e.g. {"DISTANCE": "close", "TYPE": "dust", "SOAP: "low", ...}
        data = [dict(zip(attributes, current)) for current in values]

        self.tree = create_decision_tree(data, attributes, target_attr, gain)

        defined = open(train_refill, "r")
        lines = defined.readlines()
        defined.close()

        attributes = lines.pop(0).split()  # first row represents the naming of values
        target_attr = attributes[-1]  # last column of training set represents the result
        values = [line.split() for line in lines]

        # create list of dictionaries (each dictionary consists of names of attributes and corresponding values)
        # e.g. {"DISTANCE": "close", "TYPE": "dust", "SOAP: "low", ...}
        data = [dict(zip(attributes, current)) for current in values]

        self.tree_refill = create_decision_tree(data, attributes, target_attr, gain)

    def classify(self, distance, instance, soap, battery, container,):
        collection = dict()
        collection["DISTANCE"] = distance
        collection["TYPE"] = instance
        collection["SOAP"] = soap
        collection["BATTERY"] = battery
        collection["CONTAINER"] = container
        return get_classification(self.tree, collection)

    def classify_refill(self, dist_sta, dist_bin, battery, soap, container):
        collection = dict()
        collection["DIST_STA"] = dist_sta
        collection["DIST_BIN"] = dist_bin
        collection["BATTERY"] = soap
        collection["SOAP"] = battery
        collection["CONTAINER"] = container
        return get_classification(self.tree_refill, collection)

    def draw_cleaning_tree(self):
        draw(self.tree)

    def draw_refill_tree(self):
        draw(self.tree_refill)
