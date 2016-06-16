def majority_value(data, target_attr):
    return most_frequent([record[target_attr] for record in data])


def most_frequent(data):
    """Return which result is the most common."""
    return max(unique(data), key=lambda x: data.count(x))


def unique(data):
    """Return list of unique values for given list."""
    return list(set(data))


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
    out_list = []
    
    if not data:
        return out_list
    else:
        record = data.pop()
        if record[attr] == value:
            out_list.append(record)
            out_list.extend(get_examples(data, attr, value))
            return out_list
        else:
            out_list.extend(get_examples(data, attr, value))
            return out_list


def get_classification(tree, record):
    """Return result for given record and tree, where record is a
    dictionary of attributes and corresponding values."""
    if isinstance(tree, str):
        return tree
    else:
        attr = tree.keys()[0]
        subtree = tree[attr][record[attr]]
        return get_classification(subtree, record)


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
                filter(lambda x: x != best, attributes),
                target_attr, fitness_func)
            tree[best][val] = subtree

    return tree
