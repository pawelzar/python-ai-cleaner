def fuzzy_distance(distance):
    if distance < 8:
        return 'close'
    elif distance < 14:
        return 'medium'
    return 'far'


def fuzzy_soap(soap):
    if soap < 20:
        return 'low'
    elif soap < 70:
        return 'medium'
    return 'high'


def fuzzy_battery(battery):
    if battery < 20:
        return 'low'
    elif battery < 90:
        return 'medium'
    return 'high'


def fuzzy_container(container):
    if container < 10:
        return 'empty'
    elif container < 90:
        return 'half'
    return 'full'
