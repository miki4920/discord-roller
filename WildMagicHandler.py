from Utility.UtilityHandler import read_pickle, write_pickle


class WildMagic(object):
    def __init__(self):
        self.wild_magic_dictionary = read_pickle("FileStorage/ReferenceLists/WildMagicDictionary.pickle")
        self.surge_magic_dictionary = read_pickle("FileStorage/ReferenceLists/SurgeMagicDictionary.pickle")

    def determine_wild_magic(self, roll):
        roll = [(roll, roll + 1) if roll % 2 == 1 else (roll - 1, roll)][0]
        return self.wild_magic_dictionary[roll]

    def determine_surge_magic(self, roll):
        return self.surge_magic_dictionary[roll-1]
