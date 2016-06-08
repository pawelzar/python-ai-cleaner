def majority_value(data, target_attr):
    return most_frequent([record[target_attr] for record in data])


def most_frequent(lst):
    highest_freq = 0
    most_freq = None

    for val in unique(lst):
        if lst.count(val) > highest_freq:
            most_freq = val
            highest_freq = lst.count(val)
            
    return most_freq


def unique(lst):
    unique_lst = []

    for item in lst:
        if unique_lst.count(item) <= 0:
            unique_lst.append(item)

    return unique_lst


def get_values(data, attr):
    return unique([record[attr] for record in data])


def choose_attribute(data, attributes, target_attr, fitness):
    best_gain = 0.0
    best_attr = None

    for attr in attributes:
        gain = fitness(data, attr, target_attr)
        if gain >= best_gain and attr != target_attr:
            best_gain = gain
            best_attr = attr

    return best_attr


def get_examples(information, attr, value):
    data = information[:]
    rtn_lst = []
    
    if not data:
        return rtn_lst
    else:
        record = data.pop()
        if record[attr] == value:
            rtn_lst.append(record)
            rtn_lst.extend(get_examples(data, attr, value))
            return rtn_lst
        else:
            rtn_lst.extend(get_examples(data, attr, value))
            return rtn_lst


def get_classification(tree, record):
    if isinstance(tree, str):
        return tree
    else:
        attr = tree.keys()[0]
        t = tree[attr][record[attr]]
        return get_classification(t, record)


def create_decision_tree(data, attributes, target_attr, fitness_func):
    values = [record[target_attr] for record in data]
    default = majority_value(data, target_attr)

    if not data or (len(attributes) - 1) <= 0:
        return default
    elif values.count(values[0]) == len(values):
        return values[0]
    else:
        best = choose_attribute(data, attributes, target_attr, fitness_func)

        tree = {best: {}}

        for val in get_values(data, best):
            subtree = create_decision_tree(
                get_examples(data, best, val),
                [attr for attr in attributes if attr != best],
                target_attr, fitness_func)

            tree[best][val] = subtree

    return tree
