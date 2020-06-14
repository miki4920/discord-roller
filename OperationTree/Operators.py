def add(value_one, value_two):
    return int(value_one) + int(value_two)


def sub(value_one, value_two):
    return int(value_one) - int(value_two)


def mul(value_one, value_two):
    return int(value_one) * int(value_two)


def true_div(value_one, value_two):
    return int(value_one) / int(value_two)


def floor_div(value_one, value_two):
    return int(value_one) // int(value_two)


def mod(value_one, value_two):
    return int(value_one) % int(value_two)


def bigger_than(value_one, value_two):
    value_two = int(value_two)
    print(value_one)
    if type(value_one) != int:
        value_one = value_one.roll
        return sum([roll > value_two for roll in value_one])
    return int(value_one) > value_two


def smaller_than(value_one, value_two):
    value_two = int(value_two)
    if type(value_one) != int:
        value_one = value_one.roll
        return sum([roll < value_two for roll in value_one])
    return int(value_one) < value_two


def bigger_equal_than(value_one, value_two):
    value_two = int(value_two)
    print(value_one)
    if type(value_one) != int:
        value_one = value_one.roll
        return sum([roll >= value_two for roll in value_one])
    return int(value_one) >= value_two


def smaller_equal_than(value_one, value_two):
    value_two = int(value_two)
    if type(value_one) != int:
        value_one = value_one.roll
        return sum([roll <= value_two for roll in value_one])
    return int(value_one) <= value_two