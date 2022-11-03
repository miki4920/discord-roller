import re
import random
from Utility.ErrorHandler import WrongCommandFormat, RollZero
from DiceOperations.RollFunctions.ExplodingDice import exploding_roll
from DiceOperations.RollFunctions.StandardRoll import multi_die_roll
from DiceOperations.RollFunctions.DropKeepDice import drop_keep


class Roll(object):
    def __init__(self, roll, inside_codeblock):
        self.roll = roll
        self.inside_codeblock = inside_codeblock
        self.discarded_roll = []
        self.negative = self.roll[0] == "-"
        self.handle_dice()

    def __int__(self):
        return sum(self.roll)

    def __float__(self):
        return float(sum(self.roll))

    def __str__(self):
        roll_list = []
        for number in self.roll:
            roll_list.append(str(number))
        for number in self.discarded_roll:
            if self.inside_codeblock:
                roll_list.append("".join(u'\u0336' + i for i in str(number)))
            else:
                roll_list.append("~~" + str(number) + "~~")
        random.shuffle(roll_list)
        string = ", ".join(roll_list)
        string = string[1:] if string[0:3] == " - " else string
        return "(" + string + ")"

    def handle_dice(self):
        # Check if roll is negative then separates roll into modifiers
        self.roll = re.findall("f|kl|dh|dl|d|k|!p|!!|!|kh|\d+", self.roll)
        # Check if there are any additional modifiers on a die, if not, then
        roll_modifiers = self.roll[3:] if len(self.roll) > 3 else []
        # Allows to roll dice in format "dX" where x is the die
        if len(self.roll) == 2:
            self.roll.insert(0, "1")
        # Gets all the important dice information
        try:
            self.roll = [self.roll[0], 1, self.roll[2]]
        except IndexError:
            raise WrongCommandFormat()
        # Checks if a die is a fate die
        if self.roll[2] == "f":
            self.roll = [self.roll[0], -1, 1]
        try:
            self.roll = list(map(int, self.roll))
        except ValueError:
            raise WrongCommandFormat()
        if any([die == 0 for die in self.roll]):
            raise RollZero()
        # Rolls dice and applies modifiers
        result = multi_die_roll(self.roll)
        discarded_result = []
        for modifier in roll_modifiers:
            if "!" in modifier:
                result = exploding_roll(result, self.roll, modifier)
            try:
                if "d" in modifier or "k" in modifier:
                    modifier_number = int(roll_modifiers[roll_modifiers.index(modifier) + 1])
                    result, discarded_result = drop_keep(result, modifier, modifier_number)
            except IndexError:
                raise WrongCommandFormat()
        # Makes die negative if that was intended
        self.roll = [i * (1 - (2 * self.negative)) for i in result]
        self.discarded_roll = [i * (1 - (2 * self.negative)) for i in discarded_result]

    @staticmethod
    def is_integer():
        return True
