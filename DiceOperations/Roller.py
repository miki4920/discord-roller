from DiceOperations.ShuntingYard import shunting_yard_algorithm, tokenizer
import re
from ErrorHandler import WrongCommandFormat, RollIsZero
from DiceOperations.RollFunctions.ExplodingDice import exploding_roll
from DiceOperations.RollFunctions.StandardRoll import multi_die_roll
from DiceOperations.RollFunctions.DropKeepDice import drop_keep
from DiceOperations.RollClass import Roll


def handle_dice(roll):
    roll_original = roll.roll
    roll = roll.roll
    # Check if roll is negative then separates roll into modifiers
    negative = roll[0] == "-"
    roll = re.findall("f|kl|dh|dl|d|k|!p|!!|!|kh|\d+", roll)
    # Check if there are any additional modifiers on a die, if not, then
    roll_modifiers = roll[3:] if len(roll) > 3 else []
    # Allows to roll dice in format "dX" where x is the die
    if len(roll) == 2:
        roll.insert(0, "1")
    # Gets all the important dice information
    try:
        roll = [roll[0], 1, roll[2]]
    except IndexError:
        raise WrongCommandFormat(roll_original)
    # Checks if a die is a fate die
    if roll[2] == "f":
        roll = [roll[0], -1, 1]
    try:
        roll = list(map(int, roll))
    except ValueError:
        raise WrongCommandFormat(" ".join(roll_original))
    if any([die == 0 for die in roll]):
        raise RollIsZero(roll_original)
    # Rolls dice and applies modifiers
    result = multi_die_roll(roll)
    for modifier in roll_modifiers:
        if "!" in modifier:
            result = exploding_roll(result, roll, modifier)
        try:
            if "d" in modifier or "k" in modifier:
                modifier_number = int(roll_modifiers[roll_modifiers.index(modifier) + 1])
                result = drop_keep(result, modifier, modifier_number)
        except IndexError:
            raise WrongCommandFormat(roll_original)
    # Makes die negative if that was intended
    return [i*(1-(2*negative)) for i in result]


class DiceRoll(object):
    def __init__(self):
        pass

    @staticmethod
    def dice_to_classes(tokenized_expression):
        # Converts all dice stings into classes of Roll
        for index in range(0, len(tokenized_expression)):
            if "d" in tokenized_expression[index]:
                roll = Roll(tokenized_expression[index])
                roll.roll = handle_dice(roll)
                tokenized_expression[index] = roll
        return tokenized_expression

    @staticmethod
    def dice_to_string(tokenized_expression):
        # Converts all dice to strings for the final output
        return " ".join(map(str, tokenized_expression))

    def roll_dice(self, roll):
        # Tokenizes expression and then resolves all mathematical operations
        tokenized_expression = tokenizer(roll)
        tokenized_expression = self.dice_to_classes(tokenized_expression)
        resulting_roll = shunting_yard_algorithm(tokenized_expression)
        string_roll = self.dice_to_string(tokenized_expression)
        return resulting_roll, string_roll

