from random import randint
from ShuntingYard import shunting_yard_algorithm, tokenizer


class Roll(object):
    def __init__(self, roll):
        self.roll = self.roll_dice(roll)

    @staticmethod
    def roll_dice(roll):
        roll = list(map(int, roll.split("d")))
        roll = [randint(1, roll[1]) for _ in range(0, roll[0])]
        return roll

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
