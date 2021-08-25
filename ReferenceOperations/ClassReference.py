from Utility.UtilityHandler import read_json_api
from math import ceil


def get_levels(class_json):
    class_index = class_json.get("index")
    level_features = dict((key, []) for key in range(1, 21))
    for level in range(1, 21):
        level_feature = read_json_api("level", f"{class_index}-{level}")["features"]
        for feature in level_feature:
            level_features[level].append(feature["name"])
    return level_features


def get_formatted_level_features(class_json):
    formatted_level_features = ""
    levels = get_levels(class_json)
    for level in levels:
        level_features = ', '.join(levels[level])
        if level < 10:
            level = str(level) + " "
        formatted_level_features += f"`{level}` {level_features}\n"
    return formatted_level_features + "\n"


def get_hit_points(class_json):
    name = class_json.get("name").lower()
    hit_die_value = class_json.get("hit_die")
    hit_die = "1d" + str(hit_die_value)
    hit_die_average = ceil((1+hit_die_value)/2)
    hit_point_block = f"\n**Hit Dice: ** {hit_die} per {name} level\n" \
                 f"**Hit Points at 1st Level: **{hit_die_value} + your Constitution modifier\n" \
                 f"**Hit Points at Higher Levels: **{hit_die} (or {hit_die_average}) + your Constitution modifier per {name} level after 1st\n"
    return hit_point_block + "\n"


def get_proficiencies(class_json, proficiency_type):
    proficiencies = ""
    for proficiency in class_json.get("proficiencies"):
        if proficiency["type"] == proficiency_type:
            proficiencies += proficiency["name"] + ", "
    return proficiencies


def get_proficiency_choices(class_json, proficiency_type):
    proficiency_choice = class_json.get("proficiency_choices")
    proficiencies = ""
    for proficiency_from in proficiency_choice:
        if proficiency_from["type"] == proficiency_type:
            proficiencies = f"Choose {proficiency_from['choose']} from: "
            for proficiency in proficiency_from["from"]:
                proficiencies += proficiency["name"] + ", "
    return proficiencies


def get_armor(armor):
    if not armor:
        armor = "None"
    return armor


def get_tools(tools):
    if not tools:
        tools = "None"
    return tools


def get_saving_throws(class_json):
    saving_throw_names = ""
    saving_throws = class_json.get("saving_throws")
    for saving_throw in saving_throws:
        saving_throw_names += saving_throw["name"] + ", "
    return saving_throw_names


def get_proficiencies_block(class_json):
    proficiencies = {"armor": "", "weapon": "", "tool": ""}
    proficiencies_choices = {"skills": "", "tools": ""}
    for proficiency in proficiencies:
        proficiencies[proficiency] = get_proficiencies(class_json, proficiency)
    for proficiency in proficiencies_choices:
        proficiencies_choices[proficiency] = get_proficiency_choices(class_json, proficiency)
    armor = get_armor(proficiencies["armor"]) + "\n"
    weapons = proficiencies["weapon"] + "\n"
    tools = get_tools(proficiencies["tool"] + proficiencies_choices["tools"]) + "\n"
    saving_throws = get_saving_throws(class_json) + "\n"
    skills = proficiencies_choices["skills"] + "\n\n"
    proficiency_block = f"**Armor: ** {armor}" \
                        f"**Weapons: ** {weapons}" \
                        f"**Tools: ** {tools}" \
                        f"**Saving Throws: ** {saving_throws}" \
                        f"**Skills: ** {skills}"
    return proficiency_block


def get_equipment_choices(equipment):
    equipment_choice_block = "\n"
    for item in equipment:
        item = item["from"]
        item_string = "- "
        if type(item) == dict:
            item_string += f"One of {item['equipment_category']['name']}\n"
            equipment_choice_block += item_string
        else:
            for choice in item:
                if type(choice) == list:
                    for sub_choice in choice:
                        if sub_choice.get("quantity"):
                            item_string += f"{sub_choice['quantity']} {sub_choice['name']} and "
                        else:
                            sub_choice = sub_choice['equipment_option']
                            item_string += f"{sub_choice['choose']} of {sub_choice['from']['equipment_category']['name']} and "
                    item_string = item_string[:-4] + "or "
                elif choice.get("name"):
                    item_string += f"{choice['quantity']} {choice['name']} or "
                elif choice.get("equipment_option"):
                    choice = choice['equipment_option']
                    item_string += f"{choice['choose']} of {choice['from']['equipment_category']['name']} or "
            item_string = item_string[:-3]
            equipment_choice_block += item_string + "\n"
    return equipment_choice_block


def get_starting_equipment(equipment):
    equipment_string = "- "
    for item in equipment:
        equipment_string += f"{item['quantity']} {item['name']}, "
    if equipment_string != "- ":
        return equipment_string[:-2] + "\n"
    return ""


def get_equipment_block(class_json):
    index = class_json.get("index")
    equipment = read_json_api("starting-equipment", index)
    starting_equipment = get_starting_equipment(equipment.get("starting_equipment"))
    equipment_choices = get_equipment_choices(equipment.get("starting_equipment_options"))
    equipment_block = f"{equipment_choices}" \
                      f"{starting_equipment}"
    return equipment_block


def class_reference(class_json):
    messages = []
    name = class_json.get("name")
    levels = get_formatted_level_features(class_json)
    hit_points = get_hit_points(class_json)
    proficiencies = get_proficiencies_block(class_json)
    equipment = get_equipment_block(class_json)
    class_block = f"{levels}" \
                  f"**Hit Points** {hit_points}" \
                  f"**Proficiencies** {proficiencies}" \
                  f"**Equipment** {equipment}"
    messages.append((name, class_block))
    return messages
