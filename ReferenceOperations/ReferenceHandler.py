from Utility.UtilityHandler import read_json, read_pickle
from Levenshtein import distance
from ReferenceOperations.SpellReference import spell_reference
from ReferenceOperations.MonsterReference import monster_reference
from ReferenceOperations.RaceReference import race_reference
from ReferenceOperations.ClassReference import class_reference
from ReferenceOperations.LevelReference import level_check, level_reference
from ReferenceOperations.ConditionReference import condition_reference


class ReferenceHandler(object):
    def __init__(self):
        self.spell_list = "FileStorage/ReferenceLists/SpellList.pickle"
        self.monster_list = "FileStorage/ReferenceLists/MonsterList.pickle"
        self.race_list = "FileStorage/ReferenceLists/RaceList.pickle"
        self.class_list = "FileStorage/ReferenceLists/ClassList.pickle"
        self.condition_list = "FileStorage/ReferenceLists/ConditionList.pickle"
        self.abbreviations_dictionary = {"s": "spell",
                                         "m": "monster",
                                         "r": "race",
                                         "c": "class"}
        self.item_list_dictionary = {"spell": (spell_reference, self.spell_list, 0.3),
                                     "monster": (monster_reference, self.monster_list, 0.3),
                                     "race": (race_reference, self.race_list, 0.7),
                                     "class": (class_reference, self.class_list, 0.1),
                                     "level": (level_reference, self.class_list, 0.1),
                                     "condition": (condition_reference, self.condition_list, 0.5)}

    @staticmethod
    def get_item_name(message, item_list, cutout_point):
        item_list = read_pickle(item_list)
        item_name = message.split(" ")[1:]
        item_name = " ".join([word.capitalize() for word in item_name])
        for item in item_list:
            if distance(item_name, item) / max(len(item_name),
                                               len(item)) < cutout_point or item_name in item or item in item_name:
                return item
        return ""

    @staticmethod
    def get_item_index(item_name):
        item_index = item_name.lower().replace(" ", "-").replace("'", "")
        item_index = f"{item_index}"
        return item_index

    def reference_item(self, message):
        item_name = message.split(" ")[0][1:]
        item_name = self.abbreviations_dictionary[item_name] if self.abbreviations_dictionary.get(
            item_name) else item_name
        item_tuple = self.item_list_dictionary[item_name]
        valid_item_name = self.get_item_name(message, item_tuple[1], item_tuple[2])
        valid_item_index = self.get_item_index(valid_item_name)
        if level_check(item_name, message):
            item_name = "level"
            item_tuple = self.item_list_dictionary[item_name]
            valid_item_index += "-" + message.split(" ")[2]
        if not valid_item_index:
            return [("Error", f"The {item_name.capitalize()} Does Not Exist in SRD.")]
        item_json = read_json(item_name, valid_item_index)
        return item_tuple[0](item_json)
