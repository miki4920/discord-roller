from Utility.UtilityHandler import read_json


def get_help_messages():
    commands_help = ["How to Tame Marduk", read_json("./FileStorage/ReferenceLists/CommandHelp.json")]
    return commands_help
