from random import randint
import re


class Roll(object):
    def __init__(self, roll, sign):
        self.roll = roll
        self.type = self.determine_type()
        self.sign = sign

    def determine_type(self):
        if "d" in self.roll:
            self.roll = self.roll.split("d")
            return 0
        return 1

    def __int__(self):
        if self.type == 1:
            return int(self.sign + self.roll)


class DiceRoll(object):
    def __init__(self):
        self.dice = []
        self.dice_modifier = []

    def handle_roll(self, roll):
        type_dictionary = {0: [],
                           1: []}
        roll = "+" + roll.replace(" ", "").lower()
        # Splits command string by + and -, then determines sign for each one
        for die in re.split("[+\-]", roll):
            roll_index = roll.find(die)
            if roll[roll_index - 1] == "+":
                die = Roll(die, "+")
                type_dictionary[die.type].append(die)
            elif roll[roll_index - 1] == "-":
                die = Roll(die, "-")
                type_dictionary[die.type].append(die)
        self.dice = type_dictionary[0]
        self.dice_modifier = map(int, type_dictionary[1])

    def dice_to_string(self, dice):
        formatted_string = ""
        for index in range(0, len(self.dice)):
            dice_result = list(map(str, dice[index]))
            if self.dice[index].sign == "+":
                formatted_string += " + (" + " + ".join(dice_result) + ")"
            elif self.dice[index].sign == "-":
                formatted_string += " - (" + " + ".join(dice_result) + ")"
        return formatted_string[3:]

    def roll_dice(self, roll):
        self.handle_roll(roll)
        result = []
        dice_result = 0
        for die in self.dice:
            result.append(tuple([randint(1, int(die.roll[1])) for _ in range(0, int(die.roll[0]))]))
        for index in range(0, len(self.dice)):
            if self.dice[index].sign == "+":
                dice_result += sum(result[index])
            elif self.dice[index].sign == "-":
                dice_result -= sum(result[index])
        formatted_result = self.dice_to_string(result)
        return dice_result + sum(self.dice_modifier), formatted_result
