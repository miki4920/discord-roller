from random import randint


def single_die_roll(lower_bound, upper_bound):
    return randint(lower_bound, upper_bound)


def multi_die_roll(roll_information):
    die_number = roll_information[0]
    lower_bound = roll_information[1]
    upper_bound = roll_information[2]
    return [single_die_roll(lower_bound, upper_bound) for _ in range(die_number)]
