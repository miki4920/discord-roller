from Utility.UtilityHandler import read_json_api, read_json
from Levenshtein import distance
from ReferenceOperations.SpellReference import spell_reference
from ReferenceOperations.MonsterReference import monster_reference
from ReferenceOperations.RaceReference import race_reference
from ReferenceOperations.ClassReference import class_reference
from ReferenceOperations.LevelReference import level_check, level_reference
from ReferenceOperations.ConditionReference import condition_reference


class ReferenceHandler(object):
    def __init__(self):
        self.spell_list = "FileStorage/ReferenceLists/SpellList.json"
        self.monster_list = "FileStorage/ReferenceLists/MonsterList.json"
        self.race_list = "FileStorage/ReferenceLists/RaceList.json"
        self.class_list = "FileStorage/ReferenceLists/ClassList.json"
        self.condition_list = "FileStorage/ReferenceLists/ConditionList.json"
        self.item_list_dictionary = {"spell": (spell_reference, self.spell_list, 0.1),
                                     "monster": (monster_reference, self.monster_list, 0.1),
                                     "race": (race_reference, self.race_list, 0.1),
                                     "class": (class_reference, self.class_list, 0.1),
                                     "level": (level_reference, self.class_list, 0.1),
                                     "condition": (condition_reference, self.condition_list, 0.1)}

    @staticmethod
    def get_item_name(item_name, item_list, cutout_point):
        item_list = read_json(item_list)
        item_name = item_name.title()
        for item in item_list:
            if distance(item_name, item) / max(len(item_name),
                                               len(item)) < cutout_point or item_name in item or item in item_name:
                return item
        return ""

    @staticmethod
    def get_item_index(item_name):
        item_index = item_name.lower().replace(" ", "-").replace("'", "")
        return item_index

    def reference_item(self, item_type, item_name):
        item_tuple = self.item_list_dictionary[item_type]
        valid_item_name = self.get_item_name(item_name, item_tuple[1], item_tuple[2])
        valid_item_index = self.get_item_index(valid_item_name)
        if level_check(item_type, item_name):
            item_type = "level"
            item_tuple = self.item_list_dictionary[item_type]
            valid_item_index += "-" + item_name.split(" ")[1]
        if not valid_item_index:
            return [("Error", f"The {item_name.capitalize()} Does Not Exist in SRD.")]
        item_json = read_json_api(item_type, valid_item_index)
        return item_tuple[0](item_json)
