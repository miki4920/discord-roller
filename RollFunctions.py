import re
from random import randint
from ErrorHandler import DieTooLowForExplosion, DropKeepModifierTooHigh, RollNotInteger


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
        if value_roll == (roll - 1 if exploded else roll):
            return [value_roll] + self.recursive_roll_penetrating(roll, exploded=True)
        return [value_roll]

    def exploding_roll(self, roll, modifier):
        results = []
        function_dictionary = {"!": self.recursive_roll,
                               "!!": self.recursive_roll_shadowrun,
                               "!p": self.recursive_roll_penetrating}
        for _ in range(0, roll[0]):
            results += function_dictionary[modifier](roll[1])
        return results

    @staticmethod
    def drop(result, modifier_number, function):
        for _ in range(0, modifier_number):
            result.remove(function(result))
        return result

    @staticmethod
    def keep(result, modifier_number, function):
        kept_result = []
        for _ in range(0, modifier_number):
            kept_result.append(function(result))
            result.remove(function(result))
        return kept_result

    def drop_keep(self, result, modifier, modifier_number):
        function_dictionary = {"d": (self.drop, min),
                               "dl": (self.drop, min),
                               "dh": (self.drop, max),
                               "k": (self.keep, max),
                               "kh": (self.keep, max),
                               "kl": (self.keep, min)}
        functions = function_dictionary[modifier]
        return functions[0](result, modifier_number, functions[1])

    def handle_dice(self, roll):
        roll_original = roll
        roll = re.findall("kl|dh|d|k|!p|!!|!|\d+", roll)
        roll_modifiers = []
        if len(roll) > 3:
            roll_modifiers = roll[3:]
        roll = [roll[0], roll[2]]
        try:
            roll = list(map(int, roll))
        except ValueError:
            raise RollNotInteger(roll_original)
        for modifier in roll_modifiers:
            if "!" in modifier:
                if roll[1] <= 1:
                    raise DieTooLowForExplosion(roll[1])
                result = self.exploding_roll(roll, modifier)
                break
        else:
            result = self.standard_roll(roll)
        for modifier in roll_modifiers:
            if "d" in modifier or "k" in modifier:
                modifier_number = int(roll_modifiers[roll_modifiers.index(modifier)+1])
                if modifier_number > len(result):
                    raise DropKeepModifierTooHigh(len(result), modifier_number)
                result = self.drop_keep(result, modifier, modifier_number)
                break
        return result
