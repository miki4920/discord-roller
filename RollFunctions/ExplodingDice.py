from RollFunctions.StandardRoll import single_die_roll
from ErrorHandler import DieTooLowForExplosion


def recursive_roll(die, roll):
    lower_bound = roll[1]
    upper_bound = roll[2]
    if die == upper_bound:
        new_die = single_die_roll(lower_bound, upper_bound)
        return [die] + recursive_roll(new_die, roll)
    return [die]


def recursive_roll_shadowrun(die, roll):
    lower_bound = roll[1]
    upper_bound = roll[2]
    if die == upper_bound:
        new_die = single_die_roll(lower_bound, upper_bound)
        return [sum([die] + recursive_roll_shadowrun(new_die, roll))]
    return [die]


def recursive_roll_penetrating(die, roll, exploded=False):
    lower_bound = roll[1]
    upper_bound = roll[2]
    if exploded:
        die -= 1
    if die == upper_bound - 1 if exploded else upper_bound:
        new_die = single_die_roll(lower_bound, upper_bound)
        return [die] + recursive_roll_penetrating(new_die, roll, exploded=True)
    return [die]


def exploding_roll(result, roll, modifier):
    lower_bound = roll[1]
    upper_bound = roll[2]
    if upper_bound-lower_bound <= 0:
        raise DieTooLowForExplosion(roll[1])
    results = []
    function_dictionary = {"!": recursive_roll,
                           "!!": recursive_roll_shadowrun,
                           "!p": recursive_roll_penetrating}
    for die in result:
        results += function_dictionary[modifier](die, roll)
    return results
