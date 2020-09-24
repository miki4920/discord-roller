from UtilityHandler import read_json
from math import ceil


def get_levels(class_json):
    class_index = class_json.get("index")
    level_features = dict((key, []) for key in range(1, 21))
    for level in range(1, 21):
        level_feature = read_json("level", f"{class_index}-{level}")["features"]
        for feature in level_feature:
            level_features[level].append(feature["name"])
    return level_features


def get_formatted_level_features(class_json):
    formatted_level_features = ""
    levels = get_levels(class_json)
    for level in levels:
        formatted_level_features += f"`{level}` {', '.join(levels[level])}\n"
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
    skills = proficiencies_choices["skills"] + "\n"
    proficiency_block = f"**Armor: ** {armor}" \
                        f"**Weapons: ** {weapons}" \
                        f"**Tools: ** {tools}" \
                        f"**Saving Throws: ** {saving_throws}" \
                        f"**Skills: ** {skills}"
    return proficiency_block


def class_reference(class_json):
    messages = []
    name = class_json.get("name")
    levels = get_formatted_level_features(class_json)
    hit_points = get_hit_points(class_json)
    proficiencies = get_proficiencies_block(class_json)
    class_block = f"{levels}" \
                  f"**Hit Points** {hit_points}" \
                  f"**Proficiencies** {proficiencies}"
    messages.append((name, class_block))
    return messages
