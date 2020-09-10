from FileHandler import read_json, read_pickle
from difflib import get_close_matches
from Levenshtein import distance


class ReferenceHandler(object):
    def __init__(self, api):
        self.api = api
        self.spell_list = "FileStorage/SpellList.pickle"

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

    @staticmethod
    def get_meta_string(level, school, ritual):
        string_dictionary = {0: f"{school} cantrip",
                             1: f"1st-level {school}",
                             2: f"2nd-level {school}",
                             3: f"3rd-level {school}",
                             4: f"{level}th-level {school}"}
        result_string = string_dictionary.get(level)
        if not result_string:
            result_string = string_dictionary[4]
        if ritual:
            result_string += " (ritual)"
        return result_string

    def reference_spell(self, message):
        valid_spell_name = self.get_item_name(message, self.spell_list)
        if not valid_spell_name:
            return "The Spell Does Not exist"
        valid_spell_index = self.get_item_index(valid_spell_name, "spells")
        spell_json = read_json(self.api, valid_spell_index)
        name = spell_json.get("name") + "\n"
        description = spell_json.get("desc")[0]
        level_school = self.get_meta_string(spell_json.get("level"), spell_json.get("school")["name"],  spell_json.get("ritual"))
        higher_level = spell_json.get("higher_level")
        spell_range = spell_json.get("range")
        components = " ".join(spell_json.get("components"))
        material_component = "(" + spell_json.get("material")[:-1] + ")" if spell_json.get("material") else None
        duration = "Concentration, " + spell_json.get("duration") if spell_json.get("concentration") else spell_json.get("duration")
        casting_time = spell_json.get("casting_time")
        classes = ", ".join([class_name["name"] for class_name in spell_json.get("classes")])
        subclasses = ", ".join([subclass_name["name"] for subclass_name in spell_json.get("subclasses")])
        return_string = f"_{level_school}_\n\n" \
                        f"**Casting Time:** {casting_time}\n" \
                        f"**Range:** {spell_range}\n" \
                        f"**Components:** {components} {material_component if material_component else ''}\n" \
                        f"**Duration:** {duration}\n\n" \
                        f"**Description**\n" \
                        f"{description}\n\n"
        if higher_level:
            return_string += f"**At Higher Levels. **{higher_level[0]}\n\n"
        return_string += f"**Spell Lists.** {classes}"
        if subclasses:
            return_string += "; " + subclasses
        return name, return_string
