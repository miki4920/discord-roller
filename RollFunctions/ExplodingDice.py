from RollFunctions.StandardRoll import single_die_roll
from ErrorHandler import DieTooLowForExplosion


def recursive_roll(roll):
    value_roll = single_die_roll(roll)
    if value_roll == roll:
        return [roll] + recursive_roll(roll)
    return [value_roll]


def recursive_roll_shadowrun(roll):
    value_roll = single_die_roll(roll)
    if value_roll == roll:
        return [sum([roll] + recursive_roll(roll))]
    return [value_roll]


def recursive_roll_penetrating(roll, exploded=False):
    value_roll = single_die_roll(roll)
    if exploded:
        value_roll -= 1
    if value_roll == (roll - 1 if exploded else roll):
        return [value_roll] + recursive_roll_penetrating(roll, exploded=True)
    return [value_roll]


def exploding_roll(roll, modifier):
    if roll[1] <= 1:
        raise DieTooLowForExplosion(roll[1])
    results = []
    function_dictionary = {"!": recursive_roll,
                           "!!": recursive_roll_shadowrun,
                           "!p": recursive_roll_penetrating}
    for _ in range(0, roll[0]):
        results += function_dictionary[modifier](roll[1])
    return results
