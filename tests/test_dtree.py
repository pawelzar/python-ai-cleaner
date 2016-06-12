from src.core import dtree, id3


def classify2(distance, points, equipment, struct):
    collection = dict()
    collection['Distance'] = distance
    collection['Points'] = points
    collection['Equipment'] = equipment
    return dtree.get_classification(struct, collection)


fin = open("../src/trainingset", "r")

lines = fin.readlines()
print "\n".join(lines)

attributes = map(str.strip, lines.pop(0).split(","))
target_attr = attributes[-1]
values = [map(str.strip, line.split(",")) for line in lines]
print
print attributes
print "\n".join(lines)

data = [dict(zip(attributes, current)) for current in values]

tree = dtree.create_decision_tree(data, attributes, target_attr, id3.gain)
for i, node in enumerate(str(tree).split('{')):
    print str(node).strip('}')

# print tree.keys()
# print type(tree)
print classify2("short", "1", "empty", tree)
print classify2("far", "3", "full", tree)
print classify2("short", "3", "empty", tree)
print classify2("far", "1", "full", tree)
print classify2("far", "3", "empty", tree)


def classify3(distance, instance, soap_level, battery, container, struct):
    collection = dict()
    collection['distance'] = distance
    collection['type'] = instance
    collection['soap_level'] = soap_level
    collection['battery'] = battery
    collection['container'] = container
    return dtree.get_classification(struct, collection)


fin = open("../src/train_set", "r")

lines = fin.readlines()
print "\n".join(lines)

attributes = lines.pop(0).split()
target_attr = attributes[-1]
values = [line.split() for line in lines]
print
print attributes
print "\n".join(lines)

data = [dict(zip(attributes, current)) for current in values]

tree2 = dtree.create_decision_tree(data, attributes, target_attr, id3.gain)
for i, node in enumerate(str(tree2).split('{')):
    print str(node).strip('}')

print classify3("far", "dust", "low", "full", "empty", tree2)
