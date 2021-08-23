class RollerException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{self.message}"


class DieTooLowForExplosion(RollerException):
    def __init__(self):
        message = "You must roll a d2 or higher to roll exploding dice."
        super().__init__(message)


class DivisionByZeroError(RollerException):
    def __init__(self):
        message = "At one point, you tried to divide by 0. \nPlease make sure your roll is mathematically correct"
        super().__init__(message)


class DropKeepModifierTooHigh(RollerException):
    def __init__(self):
        message = "You cannot drop/keep more dice than you roll."
        super().__init__(message)


class RollZero(RollerException):
    def __init__(self):
        message = "You cannot roll a 0 sided die."
        super().__init__(message)


class UnexpectedError(RollerException):
    def __init__(self, error):
        message = "A Marduk has encountered an unexpected error: " + error + "\nPlease copy this whole message and send it " \
                                                                             "to our support server so we may improve " \
                                                                             "this bot. "
        super().__init__(message)


class TooFewArguments(RollerException):
    def __init__(self):
        message = "You must provide at least one provide at least one value for this command."
        super().__init__(message)


class TooHighLevel(RollerException):
    def __init__(self):
        message = "You are trying to reference a level outside of 1-20 range."
        super().__init__(message)


class TooManyDice(RollerException):
    def __init__(self):
        message = "You have used too many dice.\nThis bot has a limit of 2000 characters.\nThat is equals approximately " \
                  "400d20. "
        super().__init__(message)


class TooManyOperators(RollerException):
    def __init__(self):
        message = "You have used too many operators, or maybe you have forgotten a bracket."
        super().__init__(message)


class WrongCommandFormat(RollerException):
    def __init__(self):
        message = "Your command is in wrong format.\nPlease refer to **!help-me** or **/help-me** for more information."
        super().__init__(message)
