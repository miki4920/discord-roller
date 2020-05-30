from random import randint


class DiceRoll(object):
    def __init__(self):
        self.dice = []
        self.dice_modifier = 0

    def handle_roll(self, roll):
        roll = roll.replace(" ", "").lower()
        roll = roll.split("+")
        for die in roll:
            if "d" in die:
                self.dice.append(list(map(int, die.split("d"))))
            else:
                self.dice_modifier += int(die)

    @staticmethod
    def dice_to_string(dice):
        formatted_string = ""
        for dice_result in dice:
            dice_result = list(map(str, dice_result))
            formatted_string += "(" + " + ".join(dice_result) + ") + "
        return formatted_string[0:len(formatted_string)-3]

    def roll_dice(self, roll):
        self.dice = []
        self.dice_modifier = 0
        self.handle_roll(roll)
        result = []
        for die in self.dice:
            result.append(tuple([randint(1, int(die[1])) for _ in range(0, int(die[0]))]))
        formatted_result = self.dice_to_string(result)
        return sum([sum(rolls) for rolls in result]) + self.dice_modifier, formatted_result
