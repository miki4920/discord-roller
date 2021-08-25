from Utility.UtilityHandler import read_json


class WildMagic(object):
    def __init__(self):
        self.wild_magic_dictionary = read_json("FileStorage/ReferenceLists/WildMagicDictionary.json")
        self.surge_magic_dictionary = read_json("FileStorage/ReferenceLists/SurgeMagicDictionary.json")

    def determine_wild_magic(self, roll):
        return self.wild_magic_dictionary[roll-1]

    def determine_surge_magic(self, roll):
        return self.surge_magic_dictionary[roll-1]
