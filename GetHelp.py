from UtilityHandler import read_pickle


def get_help_messages():
    commands_help = ["How to Tame Marduk", read_pickle("FileStorage/CommandHelp.pickle")]
    messages = [commands_help]
    return messages
