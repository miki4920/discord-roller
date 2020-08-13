from FileHandler import read_file


class WildMagic(object):
    def __init__(self):
        self.wild_magic_dictionary = read_file("FileStorage/WildMagicDictionary.pickle")

    def determine_wild_magic(self, roll):
        roll = [(roll, roll + 1) if roll % 2 == 1 else (roll - 1, roll)][0]
        return self.wild_magic_dictionary[roll]
