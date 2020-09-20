from UtilityHandler import read_json, read_pickle
from Levenshtein import distance
from ReferenceOperations.SpellReference import spell_reference
from ReferenceOperations.MonsterReference import monster_reference
from ReferenceOperations.RaceReference import race_reference


class ReferenceHandler(object):
    def __init__(self):
        self.spell_list = "FileStorage/ReferenceLists/SpellList.pickle"
        self.monster_list = "FileStorage/ReferenceLists/MonsterList.pickle"
        self.race_list = "FileStorage/ReferenceLists/RaceList.pickle"
        self.item_list_dictionary = {"spell": (self.spell_list, spell_reference, 0.3),
                                     "monster": (self.monster_list, monster_reference, 0.3),
                                     "race": (self.race_list, race_reference, 0.7)}

    @staticmethod
    def get_item_name(message, item_list, cutout_point):
        item_list = read_pickle(item_list)
        item_name = message.split(" ")[1:]
        item_name = " ".join([word.capitalize() for word in item_name])
        for item in item_list:
            if distance(item_name, item) / max(len(item_name),
                                               len(item)) < cutout_point or item_name in item or item in item_name:
                return item
        return False

    @staticmethod
    def get_item_index(item_name):
        item_index = item_name.lower().replace(" ", "-").replace("'", "")
        item_index = f"{item_index}"
        return item_index

    def reference_item(self, message):
        item_name = message.split(" ")[0][1:]
        item_tuple = self.item_list_dictionary[item_name]
        valid_item_name = self.get_item_name(message, item_tuple[0], item_tuple[2])
        if not valid_item_name:
            return [("Error", f"The {item_name.capitalize()} Does Not Exist in SRD.")]
        valid_item_index = self.get_item_index(valid_item_name)
        item_json = read_json(item_name, valid_item_index)
        return item_tuple[1](item_json)
