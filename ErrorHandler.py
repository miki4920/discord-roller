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


class DropKeepModifierTooHigh(Exception):
    def __init__(self, dice_number, modifier, message="You cannot drop/keep more dice than you roll."):
        self.dice_number = dice_number
        self.modifer = modifier
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} Number of Dice: {self.dice_number}, Number you want to drop/keep: {self.modifer}"


class NoDungeonMaster(Exception):
    def __init__(self, message="There is no person on your server with a rank: DM.\nPlease refer to !h for more "
                               "information."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class RollNotInteger(Exception):
    def __init__(self, roll, message="One of the rolls is in wrong format.\nPlease refer to !h for more "
                                     "information."):
        self.roll = roll
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} Details: {self.roll}"
