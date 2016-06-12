from src.core.dtree import create_decision_tree, get_classification
from src.core.id3 import gain


class Classification:
    def __init__(self, file_path):
        defined = open(file_path, "r")
        lines = defined.readlines()
        defined.close()

        attributes = lines.pop(0).split()  # first row represents the naming of values
        target_attr = attributes[-1]  # last column of training set represents the result
        values = [line.split() for line in lines]

        # create list of dictionaries (each dictionary consists of names of attributes and corresponding values)
        # e.g. {"distance": "close", "type": "dust", "soap: "low", ...}
        data = [dict(zip(attributes, current)) for current in values]

        self.tree = create_decision_tree(data, attributes, target_attr, gain)

    def classify(self, distance, instance, soap, battery, container,):
        collection = dict()
        collection['distance'] = distance
        collection['type'] = instance
        collection['soap'] = soap
        collection['battery'] = battery
        collection['container'] = container
        return get_classification(self.tree, collection)
