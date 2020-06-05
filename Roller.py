from random import randint
from ShuntingYard import shunting_yard_algorithm, tokenizer
import re


class Roll(object):
    def __init__(self, roll):
        self.roll = self.handle_dice(roll)

    @staticmethod
    def standard_roll(roll):
        return [randint(1, roll[1]) for _ in range(0, roll[0])]

    def recursive_roll(self, roll):
        value_roll = randint(1, roll)
        if value_roll == roll:
            return [roll] + self.recursive_roll(roll)
        return [value_roll]

    def recursive_roll_shadowrun(self, roll):
        value_roll = randint(1, roll)
        if value_roll == roll:
            return [sum([roll] + self.recursive_roll(roll))]
        return [value_roll]

    def exploding_roll(self, roll, modifier):
        results = []
        for _ in range(0, roll[0]):
            if modifier == "!":
                results += self.recursive_roll(roll[1])
            elif modifier == "!!":
                results += self.recursive_roll_shadowrun(roll[1])
        return results

    def handle_dice(self, roll):
        roll = re.findall("!!|!|\d+", roll)
        roll_modifiers = []
        if len(roll) > 2:
            roll_modifiers = roll[2:]
            roll = roll[0:2]
        roll = list(map(int, roll))
        for modifier in roll_modifiers:
            if modifier in ["!", "!!"]:
                if roll[1] <= 1:
                    raise ValueError
                return self.exploding_roll(roll, modifier)
        return self.standard_roll(roll)

    def __int__(self):
        return sum(self.roll)

    def __str__(self):
        return "(" + " + ".join(map(str, self.roll)) + ")"


class DiceRoll(object):
    def __init__(self):
        pass

    @staticmethod
    def dice_to_classes(tokenized_expression):
        for index in range(0, len(tokenized_expression)):
            if "d" in tokenized_expression[index]:
                tokenized_expression[index] = Roll(tokenized_expression[index])
        return tokenized_expression

    @staticmethod
    def dice_to_string(tokenized_expression):
        return " ".join(map(str, tokenized_expression))

    def roll_dice(self, roll):
        tokenized_expression = tokenizer(roll)
        tokenized_expression = self.dice_to_classes(tokenized_expression)
        resulting_roll = shunting_yard_algorithm(tokenized_expression)
        string_roll = self.dice_to_string(tokenized_expression)
        return resulting_roll, string_roll
