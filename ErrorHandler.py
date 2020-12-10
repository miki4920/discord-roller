class RollerException(Exception):
    def __init__(self, command, message):
        self.command = command
        self.message = message

    def __str__(self):
        return f"{self.message}\nYour Command: {self.command}"


def command_not_existing():
    message = "The command you tried to use does not exist.\nPlease type **!h** for more information."
    return RollerException("", message)


def die_too_low_for_explosion():
    message = "You must roll a d2 or higher to roll exploding dice."
    return RollerException("", message)


def division_by_zero_error():
    message = "At one point, you tried to divide by 0. \nPlease make sure your roll is mathematically correct"
    return RollerException("", message)


def drop_keep_modifier_too_high():
    message = "You cannot drop/keep more dice than you roll."
    return RollerException("", message)


def roll_is_zero():
    message = "You cannot roll a 0 sided die."
    return RollerException("", message)


def unexpected_error(error):
    message = "A Marduk has encountered an unexpected error: " + error + "\nPlease copy this whole message and send it " \
                                                                         "to our support server so we may improve " \
                                                                         "this bot. "
    return RollerException("", message)


def too_high_level():
    message = "You are trying to reference a level outside of 1-20 range."
    return RollerException("", message)


def too_many_dice():
    message = "You have used too many dice.\nThis bot has a limit of 2000 characters.\nThat is equals approximately " \
              "400d20. "
    return RollerException("", message)


def too_many_operators():
    message = "You have used too many operators, or maybe you have forgotten a bracket."
    return RollerException("", message)


def wrong_command_format():
    message = "Your command is in wrong format.\nPlease refer to **!h** for more information."
    return RollerException("", message)
