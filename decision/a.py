import dtree
import id3


def classify2(distance, points, equipment, struct):
    collection = dict()
    collection['Distance'] = distance
    collection['Points'] = points
    collection['Equipment'] = equipment
    return dtree.get_classification(struct, collection)


fin = open("trainingset", "r")

lines = [line.strip() for line in fin.readlines()]

lines.reverse()
attributes = [attr.strip() for attr in lines.pop().split(",")]
target_attr = attributes[-1]
lines.reverse()

data = []
for line in lines:
    data.append(dict(zip(attributes,
                         [datum.strip() for datum in line.split(",")])))

tree = dtree.create_decision_tree(data, attributes, target_attr, id3.gain)
for i, node in enumerate(str(tree).split('{')):
    print str(node).strip('}')

#print tree.keys()
#print type(tree)
print classify2("short", "1", "empty", tree)
print classify2("far", "3", "full", tree)
#print dtree.get_classification(["short", "1", "empty"], tree)
