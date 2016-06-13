from src.core.dtree import create_decision_tree
from src.core.id3 import gain
from src.extra.draw import draw_tree


def create_cleaning_set():
    train_set = open("../train", "w")
    train_set.write("DISTANCE    TYPE    SOAP    BATTERY    CONTAINER    CLEAN" + "\n")

    for distance in ["close", "medium", "far"]:
        for instance in ["dust", "cat", "water"]:
            for soap in ["low", "medium", "high"]:
                for battery in ["low", "medium", "high"]:
                    for container in ["empty", "half", "full"]:
                        # result = {"low": "False"}.get(battery, "True")
                        result = "False" if battery == "low" else \
                            ("False" if (instance == "cat" or instance == "water") and soap == "low"
                             else "False" if container == "full" else "True")
                        line = (distance.ljust(12, " ") +
                                instance.ljust(8, " ") +
                                soap.ljust(8, " ") +
                                battery.ljust(11, " ") +
                                container.ljust(13, " "))
                        train_set.write(line + result + "\n")

    train_set.close()


def create_refill_set():
    train_set = open("../train_refill", "w")
    train_set.write("DIST_STA    DIST_BIN    BATTERY    SOAP    CONTAINER    DECISION" + "\n")

    for dist_station in ["close", "medium", "far"]:
        for dist_bin in ["close", "medium", "far"]:
            for battery in ["low", "medium", "high"]:
                for soap in ["low", "medium", "high"]:
                    for container in ["empty", "half", "full"]:
                        # result = {"low": "False"}.get(battery, "True")
                        '''result = "bin" if ((dist_bin == "close" or dist_bin == "medium") and
                                           (dist_station == "medium" or dist_station == "far") and
                                           container == "full") \
                            else "station"'''
                        result = "bin" if container == "full" else "station"
                        line = (dist_station.ljust(12, " ") +
                                dist_bin.ljust(12, " ") +
                                battery.ljust(11, " ") +
                                soap.ljust(8, " ") +
                                container.ljust(13, " "))
                        train_set.write(line + result + "\n")

    train_set.close()


def shuffle_set():
    defined = open("../train_refill", "r")
    lines = defined.readlines()
    defined.close()

    attributes = lines.pop(0).split()  # first row represents the naming of values
    target_attr = attributes[-1]  # last column of training set represents the result
    values = [line.split() for line in lines]

    data = [dict(zip(attributes, current)) for current in values]
    cleaning_tree = create_decision_tree(data, attributes, target_attr, gain)
    draw_tree(cleaning_tree)
    new_cleaning_set = data[:]

    i = 1
    while i < len(data):
        temp = new_cleaning_set[1:i] + new_cleaning_set[i+1:]
        if cleaning_tree == create_decision_tree(temp, attributes, target_attr, gain):
            new_cleaning_set = new_cleaning_set[1:i] + new_cleaning_set[i+1:]
        i += 1
    draw_tree(create_decision_tree(new_cleaning_set, attributes, target_attr, gain))
    train_set = open("../train_test2", "w")
    for i in new_cleaning_set:
        line = ""
        print list(i.items())
        val = i.values()
        line = (val[3].ljust(12, " ") +
                val[4].ljust(12, " ") +
                val[1].ljust(11, " ") +
                val[5].ljust(8, " ") +
                val[0].ljust(13, " ") + val[2])
        train_set.write(line + "\n")
    train_set.close()

# create_cleaning_set()
# create_refill_set()
shuffle_set()
