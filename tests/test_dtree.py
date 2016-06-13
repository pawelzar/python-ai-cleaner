from src.core import dtree, id3


def classify(distance, instance, soap_level, battery, container, struct):
    collection = dict()
    collection["DISTANCE"] = distance
    collection["TYPE"] = instance
    collection["SOAP"] = soap_level
    collection["BATTERY"] = battery
    collection["CONTAINER"] = container
    return dtree.get_classification(struct, collection)


fin = open("../src/train_cleaning", "r")

lines = fin.readlines()
# print "\n".join(lines)

attributes = lines.pop(0).split()
target_attr = attributes[-1]
values = [line.split() for line in lines]
# print
# print attributes
# print "\n".join(lines)

data = [dict(zip(attributes, current)) for current in values]

tree2 = dtree.create_decision_tree(data, attributes, target_attr, id3.gain)
for i, node in enumerate(str(tree2).split('{')):
    print str(node).strip('}')

print classify("far", "dust", "low", "high", "empty", tree2)
