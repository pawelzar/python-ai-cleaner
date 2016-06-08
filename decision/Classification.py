import dtree
import id3


def fuzzy_equipment(capacity, equipment):
    fill = float(equipment) / capacity
    if fill < 0.5:
        return 'empty'
    elif fill < 0.8:
        return 'almost full'
    else:
        return 'full'


def fuzzy_distance(size, distance):
    dist = float(distance) / size
    if dist < 0.4:
        return 'short'
    elif dist < 0.7:
        return 'medium'
    else:
        return 'far'


class Classification:
    def __init__(self, train):
        fin = open(train, "r")

        lines = [line.strip() for line in fin.readlines()]

        lines.reverse()
        attributes = [attr.strip() for attr in lines.pop().split(",")]
        target_attr = attributes[-1]
        lines.reverse()

        data = []
        for line in lines:
            data.append(dict(zip(attributes,
                                 [datum.strip() for datum in line.split(",")])))

        self.tree = dtree.create_decision_tree(data, attributes, target_attr, id3.gain)

    def classify(self, distance, points, equipment):
        collection = dict()
        collection['Distance'] = distance
        collection['Points'] = points
        collection['Equipment'] = equipment
        return dtree.get_classification(self.tree, collection)
