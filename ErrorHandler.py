class CommandNotExisting(Exception):
    def __init__(self, command, message="The command you tried to use does not exist.\nPlease type: !h for more "
                                        "information."):
        self.command = command
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} Details: {self.command}"


class DieTooLowForExplosion(Exception):
    def __init__(self, die, message="You must roll a d2 or higher to roll exploding dice."):
        self.die = die
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} Current die: d{self.die}"


class DivisionByZeroError(Exception):
    def __init__(self, roll, message="At one point, you tried to divide by 0. Please make sure your roll is "
                                     "mathematically correct."):
        self.roll = roll
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} Details: {self.roll}"


class DropKeepModifierTooHigh(Exception):
    def __init__(self, dice_number, modifier, message="You cannot drop/keep more dice than you roll."):
        self.dice_number = dice_number
        self.modifer = modifier
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} Number of Dice: {self.dice_number}, Number you want to drop/keep: {self.modifer}"


class RollIsZero(Exception):
    def __init__(self, roll, message="You cannot roll a d0.\nPlease refer to !h for more "
                                     "information."):
        self.roll = roll
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} Details: {self.roll}"


class TooHighLevel(Exception):
    def __init__(self, level, message="You are trying to reference a level outside of 1-20 range. Please try again.\n"):
        self.level = level
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} Referenced Level: {self.level}"


class TooManyDice(Exception):
    def __init__(self, roll, message="You have used too many dice.\nThis bot has a limit of 2000 characters.\nThat is "
                                     "approximately 400d20."):
        self.roll = roll
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} Details: {self.roll}"


class TooManyOperators(Exception):
    def __init__(self, roll, message="You have either used too many operators and brackets or too few values.\nPlease "
                                     "refer to !h for more information."):
        self.roll = " ".join(map(str, roll))
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} Details: {self.roll}"


class WrongCommandFormat(Exception):
    def __init__(self, command, message="Your command is in wrong format.\nPlease refer to !h for more "
                                        "information."):
        self.command = "".join(map(str, command))
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} Details: {self.command}"


# class UnexpectedError(Exception):
#     def __init__(self, command, message="Marduk has encountered a problem even he cannot solve. You must now travel "
#                                         "to the support server and bless them with a message below."):
#         self.command = command
#         self.message = message
#         self.error_message = str(Exception)
#         super().__init__(self.message)
#
#     def __str__(self):
#         return f"{self.message}\n{self.error_message}\n{self.command}"
