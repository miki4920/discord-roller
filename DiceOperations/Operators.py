from ErrorHandler import DivisionByZeroError


def add(value_one, value_two):
    return float(value_one) + float(value_two)


def sub(value_one, value_two):
    return float(value_one) - float(value_two)


def mul(value_one, value_two):
    return float(value_one) * float(value_two)


def true_div(value_one, value_two):
    try:
        return float(value_one) / float(value_two)
    except ZeroDivisionError:
        raise DivisionByZeroError(f"{value_one}/{value_two}")


def floor_div(value_one, value_two):
    try:
        return float(value_one) // float(value_two)
    except ZeroDivisionError:
        raise DivisionByZeroError(f"{value_one}//{value_two}")


def mod(value_one, value_two):
    return float(value_one) % float(value_two)


# Operators below are used to compare whether dice have certain value. If the condition is true, return 1,
# else return 0.
def bigger_than(value_one, value_two):
    value_two = float(value_two)
    if type(value_one) != int and type(value_one) != float:
        value_one = value_one.roll
        return sum([roll > value_two for roll in value_one])
    return float(value_one) > value_two


def smaller_than(value_one, value_two):
    value_two = float(value_two)
    if type(value_one) != int and type(value_one) != float:
        value_one = value_one.roll
        return sum([roll < value_two for roll in value_one])
    return float(value_one) < value_two


def bigger_equal_than(value_one, value_two):
    value_two = float(value_two)
    if type(value_one) != int and type(value_one) != float:
        value_one = value_one.roll
        return sum([roll >= value_two for roll in value_one])
    return float(value_one) >= value_two


def smaller_equal_than(value_one, value_two):
    value_two = float(value_two)
    if type(value_one) != int and type(value_one) != float:
        value_one = value_one.roll
        return sum([roll <= value_two for roll in value_one])
    return float(value_one) <= value_two
