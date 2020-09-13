from FileHandler import read_json, read_pickle
from difflib import get_close_matches
from Levenshtein import distance
from ReferenceOperations.SpellReference import spell_reference
from ReferenceOperations.MonsterReference import monster_reference


class ReferenceHandler(object):
    def __init__(self, api):
        self.api = api
        self.spell_list = "FileStorage/SpellList.pickle"
        self.monster_list = "FileStorage/MonsterList.pickle"
        self.item_list_dictionary = {"spell": (self.spell_list, spell_reference),
                                     "monster": (self.monster_list, monster_reference)}

    @staticmethod
    def get_item_name(message, item_list):
        item_list = read_pickle(item_list)
        item_name = message.split(" ")[1:]
        item_name = " ".join([word.capitalize() for word in item_name])
        if item_name in item_list:
            return item_name
        for item_part in item_name.split(" "):
            for item in item_list:
                for piece in item.split(" "):
                    if item_part == piece:
                        if len(item_name.split(" ")) > 1:
                            if distance(item_name, item)/len(item_name) < 0.3:
                                return item
                        else:
                            return item
        closest_item_names = get_close_matches(item_name, item_list, cutoff=0.1)
        closest_item_names = [name for name in closest_item_names if item_name in name]
        if len(closest_item_names) == 0:
            return False
        return closest_item_names[0]

    @staticmethod
    def get_item_index(item_name, category):
        item_index = item_name.lower().replace(" ", "-").replace("'", "")
        item_index = f"{category}/{item_index}"
        return item_index

    def reference_item(self, message):
        item_name = message.split(" ")[0][1:]
        item_tuple = self.item_list_dictionary[item_name]
        valid_item_name = self.get_item_name(message, item_tuple[0])
        if not valid_item_name:
            return f"The {item_name.capitalize()} Does Not Exist"
        valid_item_index = self.get_item_index(valid_item_name, item_name+"s")
        item_json = read_json(self.api, valid_item_index)
        return item_tuple[1](item_json)


