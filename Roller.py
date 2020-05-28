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
                try:
                    self.dice.append(list(map(int, die.split("d"))))
                except TypeError:
                    print(f"A type error has occurred: {roll}")
            else:
                self.dice_modifier += int(die)

    def roll_dice(self, roll):
        self.dice = []
        self.dice_modifier = 0
        self.handle_roll(roll)
        result = ()
        for die in self.dice:
            for rolls in range(0, int(die[0])):
                result += tuple([randint(1, int(die[1]))])
        return sum(result) + self.dice_modifier, result
