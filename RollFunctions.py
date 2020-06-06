import re
from random import randint


class Roll(object):
    def __init__(self, roll):
        self.roll = self.handle_dice(roll)

    def __int__(self):
        return sum(self.roll)

    def __str__(self):
        return "(" + " + ".join(map(str, self.roll)) + ")"

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

    def recursive_roll_penetrating(self, roll, exploded=False):
        value_roll = randint(1, roll)
        if exploded:
            value_roll -= 1
        if value_roll == (roll-1 if exploded else roll):
            return [value_roll] + self.recursive_roll_penetrating(roll, exploded=True)
        return [value_roll]

    def exploding_roll(self, roll, modifier):
        results = []
        for _ in range(0, roll[0]):
            if modifier == "!":
                results += self.recursive_roll(roll[1])
            elif modifier == "!!":
                results += self.recursive_roll_shadowrun(roll[1])
            elif modifier == "!p":
                results += self.recursive_roll_penetrating(roll[1])
        return results

    def handle_dice(self, roll):
        roll = re.findall("!p|!!|!|\d+", roll)
        roll_modifiers = []
        if len(roll) > 2:
            roll_modifiers = roll[2:]
            roll = roll[0:2]
        roll = list(map(int, roll))
        for modifier in roll_modifiers:
            if "!" in modifier:
                if roll[1] <= 1:
                    raise ValueError
                return self.exploding_roll(roll, modifier)
        return self.standard_roll(roll)
