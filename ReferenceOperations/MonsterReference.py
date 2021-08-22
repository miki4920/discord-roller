from math import floor
from Utility.UtilityHandler import read_pickle


def ability_conversion(ability_score):
    ability_score = str(floor(int(ability_score) / 2) - 5)
    if int(ability_score) > -1:
        ability_score = "+" + ability_score
    return ability_score


def get_hit_points_calculation(hit_dice, constitution):
    constitution_modifier = int(ability_conversion(constitution))
    hit_points_modifier = constitution_modifier * int(hit_dice.split("d")[0])
    return f"{hit_dice} + {hit_points_modifier}"


def get_speed(speed):
    return_string = ""
    for speed_type in speed:
        if speed_type == "walk":
            return_string += speed[speed_type]
        else:
            return_string += f"{speed_type} {speed[speed_type]}"
        return_string += ", "
    return return_string[:-2] + "\n"


def get_ability_scores(monster_json):
    ability_scores = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    ability_scores_list = []
    for ability in ability_scores:
        ability_score = monster_json.get(ability)
        ability_string = f"**{ability[:3].upper()}**: {ability_score} ({ability_conversion(ability_score)})"
        ability_scores_list.append(ability_string)
    ability_scores_list.insert(3, "\n")
    ability_scores_list = " ".join(ability_scores_list)
    return ability_scores_list + "\n"


def get_proficiencies(proficiencies):
    saving_throws = []
    skills = []
    return_string = ""
    for proficiency in proficiencies:
        value = proficiency['value']
        if value > 0:
            value = "+" + str(value)
        if "Saving Throw" in proficiency["name"]:
            saving_throws.append(f"{proficiency['name'][-3:]}: {value}")
        else:
            skills.append(f"{proficiency['name'][7:]}: {value}")
    if saving_throws:
        return_string += "**Saving Throws:** " + ", ".join(saving_throws) + "\n"
    if skills:
        return_string += "**Skills:** " + ", ".join(skills) + "\n"
    return return_string


def get_senses(senses):
    return_string = "**Senses:** "
    for sense in senses:
        return_string += f"{sense.capitalize().replace('_', ' ')}: {senses[sense]}, "
    return return_string[:-2] + "\n"


def get_damage_conditions(damage_conditions):
    return_string = ""
    vulnerabilities, resistances, immunities, conditions = damage_conditions
    if vulnerabilities:
        return_string += "**Vulnerabilities:** " + ", ".join(vulnerabilities) + "\n"
    if resistances:
        return_string += "**Resistances:** " + ", ".join(resistances) + "\n"
    if immunities:
        return_string += "**Immunities:** " + ", ".join(immunities) + "\n"
    if conditions:
        conditions = [condition["name"] for condition in conditions]
        return_string += "**Conditions Immunities:** " + ", ".join(conditions) + "\n"
    return return_string


def get_languages(languages):
    if languages:
        return "**Languages:** " + languages + "\n"
    return ""


def get_xp(challenge_rating):
    xp = read_pickle("FileStorage/ReferenceLists/XPList.pickle").get(str(challenge_rating))
    if not xp:
        xp = 0
    return f"**CR**: {challenge_rating} ({xp} XP)" + "\n\n"


def get_special_abilities(special_abilities):
    return_string = ""
    if special_abilities:
        return_string = "**Special Abilities:**\n"
        for special_ability in special_abilities:
            return_string += f"**{special_ability['name']}"
            usage = special_ability.get("usage")
            if usage:
                return_string += f" ({usage['times']}/{usage['type'].capitalize()}):** {special_ability['desc']}\n\n"
            else:
                return_string += f"** {special_ability['desc']}\n\n"
    return return_string


def get_stat_block(monster_json):
    name = monster_json.get("name") + "\n"
    size = monster_json.get("size")
    monster_type = monster_json.get("type")
    alignment = monster_json.get("alignment") + "*\n\n"
    armor_class = str(monster_json.get("armor_class")) + "\n"
    hit_points_average = str(monster_json.get("hit_points"))
    hit_points_calculations = "(" + str(
        get_hit_points_calculation(monster_json.get("hit_dice"), monster_json.get("constitution"))) + ")\n"
    speed = get_speed(monster_json.get("speed"))
    ability_scores_string = get_ability_scores(monster_json)
    proficiencies = get_proficiencies(monster_json.get("proficiencies"))
    senses = get_senses(monster_json.get("senses"))
    damage_conditions = get_damage_conditions((monster_json.get("damage_vulnerabilities"),
                                               monster_json.get("damage_resistances"),
                                               monster_json.get("damage_immunities"),
                                               monster_json.get("condition_immunities")))
    languages = get_languages(monster_json.get("languages"))
    xp = get_xp(monster_json.get("challenge_rating"))
    special_abilities = get_special_abilities(monster_json.get("special_abilities"))
    stat_block = f"*{size} {monster_type}, {alignment}" \
                 f"**AC**: {armor_class}" \
                 f"**HP**: {hit_points_average} {hit_points_calculations}" \
                 f"**Speed**: {speed}" \
                 f"{ability_scores_string}" \
                 f"{proficiencies}" \
                 f"{senses}" \
                 f"{damage_conditions}" \
                 f"{languages}" \
                 f"{xp}" \
                 f"{special_abilities}"
    return name, stat_block


def get_action_block(name, actions):
    action_block = ""
    action_block_two = ""
    too_large = False
    for action in actions:
        if len(action_block + f"**{action['name']}**\n{action['desc']}\n\n") > 2000:
            too_large = True
        if not too_large:
            action_block += f"**{action['name']}**\n{action['desc']}\n\n"
        else:
            action_block_two += f"**{action['name']}**\n{action['desc']}\n\n"
    messages = [(name, action_block)]
    if too_large:
        messages.append(("", action_block_two))
    return messages


def monster_reference(monster_json):
    messages = [get_stat_block(monster_json)]
    messages.extend(get_action_block("Actions", monster_json.get("actions")))
    if monster_json.get("legendary_actions"):
        messages.extend(get_action_block("Legendary Actions", monster_json.get("legendary_actions")))
    return messages
