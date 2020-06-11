class Roll(object):
    def __init__(self, roll):
        self.roll = roll

    def __int__(self):
        return sum(self.roll)

    def __str__(self):
        string = ""
        for number in self.roll:
            if number >= 0:
                string += " + " + str(number)
            else:
                string += " - " + str(abs(number))
        string = string[3:] if string[0:3] == " + " else string[1:]
        return "(" + string + ")"
