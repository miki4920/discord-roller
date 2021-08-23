from DiceOperations.RollClass import Roll
from DiceOperations.ShuntingYard import shunting_yard_algorithm, tokenizer
from Utility.ErrorHandler import TooManyDice


class DiceRoll(object):
    def __init__(self):
        pass

    @staticmethod
    def dice_to_classes(tokenized_expression):
        # Converts all dice stings into classes of Roll
        for index in range(0, len(tokenized_expression)):
            if "d" in tokenized_expression[index]:
                roll = Roll(tokenized_expression[index])
                tokenized_expression[index] = roll
        return tokenized_expression

    @staticmethod
    def dice_to_string(tokenized_expression):
        # Converts all dice to strings for the final output
        return " ".join(map(str, tokenized_expression))

    def roll_dice(self, roll):
        # Converts expression into tokens and then resolves all mathematical operations
        tokenized_expression = tokenizer(roll)
        tokenized_expression = self.dice_to_classes(tokenized_expression)
        resulting_roll = shunting_yard_algorithm(tokenized_expression)
        string_roll = self.dice_to_string(tokenized_expression)
        if len(str(resulting_roll) + string_roll) >= 1900:
            raise TooManyDice()
        return resulting_roll, string_roll
