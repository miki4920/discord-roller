from FileHandler import import_json


class ReferenceHandler(object):
    def __init__(self, api):
        self.api = api

    def get_message_item(self, message):
        message = message.content.split(" ")
        message = message[1:]
        message = "-".join(message).lower()
        message += "/"
        return message

    def get_level_string(self, level, school, ritual):
        level = str(level)
        string_dictionary = {"0": f"{school} cantrip",
                             "1": f"1st-level {school}",
                             "2": f"2nd-level {school}",
                             "3": f"3rd-level {school}",
                             "4-9": f"{level}th-level {school}"}
        result_string = string_dictionary.get(level)
        if not result_string:
            result_string = string_dictionary["4-9"]
        if ritual:
            result_string += " (ritual)"
        return result_string

    def reference_spell(self, spell):
        spell = self.get_message_item(spell)
        spell = "spells/" + spell
        spell_json = import_json(self.api, spell)
        if spell_json.get("error"):
            return "The Spell Does Not Exist"
        if spell_json.get("count"):
            return "Multiple Matches Found"
        name = spell_json.get("name") + "\n"
        description = spell_json.get("desc")[0]
        level_school = self.get_level_string(spell_json.get("level"), spell_json.get("school")["name"],  spell_json.get("ritual"))
        higher_level = spell_json.get("higher_level")
        spell_range = spell_json.get("range")
        components = " ".join(spell_json.get("components"))
        material_component = spell_json.get("material")
        if material_component:
            material_component = "(" + material_component[:-1] + ")"
        concentration = spell_json.get("concentration")
        duration = spell_json.get("duration")
        if concentration:
            duration = "Concentration, " + duration
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
