from random import randint


def single_die_roll(upper_bound, lower_bound=1):
    return randint(lower_bound, upper_bound)


def multi_die_roll(die_number, upper_bound, lower_bound=1):
    return [single_die_roll(upper_bound, lower_bound) for _ in range(die_number)]