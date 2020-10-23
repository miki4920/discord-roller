from UtilityHandler import read_pickle


def get_help_messages():
    commands_help = ["Commands", read_pickle("FileStorage/CommandHelp.pickle")]
    modifier_help = ["Modifiers", read_pickle("FileStorage/ModifierHelp.pickle")]
    messages = [commands_help, modifier_help]
    return messages
