from DiceOperations.RollFunctions.StandardRoll import single_die_roll
from ErrorHandler import die_too_low_for_explosion


def recursive_roll(die, roll):
    # Rolls a die between 2 values, if a die is equal to the upper bound, it rolls again and adds the die to the list
    lower_bound = roll[1]
    upper_bound = roll[2]
    if die == upper_bound:
        new_die = single_die_roll(lower_bound, upper_bound)
        return [die] + recursive_roll(new_die, roll)
    return [die]


def recursive_roll_shadowrun(die, roll):
    # Rolls a die between 2 values, if a die is equal to the upper bound, it rolls again and adds the die to the
    # previous one
    lower_bound = roll[1]
    upper_bound = roll[2]
    if die == upper_bound:
        new_die = single_die_roll(lower_bound, upper_bound)
        return [sum([die] + recursive_roll_shadowrun(new_die, roll))]
    return [die]


def recursive_roll_penetrating(die, roll, exploded=False):
    # Rolls a die between 2 values, if a die is equal to the upper bound, it rolls again and adds it to the list.
    # The maximum value of exploded dice is always lower by 1
    lower_bound = roll[1]
    upper_bound = roll[2]
    if exploded:
        die -= 1
    if die == upper_bound - 1 if exploded else upper_bound:
        new_die = single_die_roll(lower_bound, upper_bound)
        return [die] + recursive_roll_penetrating(new_die, roll, exploded=True)
    return [die]


def exploding_roll(result, roll, modifier):
    # Handles exploding dice
    lower_bound = roll[1]
    upper_bound = roll[2]
    # Checks if the die difference is bigger than 1 (Prevents infinite explosion)
    if upper_bound-lower_bound <= 0:
        raise die_too_low_for_explosion()
    results = []
    # Contains all exploding functions, easily expandable
    function_dictionary = {"!": recursive_roll,
                           "!!": recursive_roll_shadowrun,
                           "!p": recursive_roll_penetrating}
    for die in result:
        results += function_dictionary[modifier](die, roll)
    return results
