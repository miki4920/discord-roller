from math import floor


def stat_conversion(ability_score):
    ability_score = floor(int(ability_score) / 2) - 5
    return ability_score


def get_hit_points_calculation(hit_dice, constitution):
    constitution_modifier = stat_conversion(constitution)
    hit_points_modifier = constitution_modifier * int(hit_dice.split("d")[0])
    return f"{hit_dice} + {hit_points_modifier}"


def get_speed_string(speed):
    return_string = ""
    for speed_type in speed:
        if speed_type == "walk":
            return_string += speed[speed_type]
        else:
            return_string += f"{speed_type} {speed[speed_type]}"
        return_string += ", "
    return return_string[:-2]


def get_ability_scores_string(monster_json):
    ability_scores = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    ability_scores_list = []
    for ability in ability_scores:
        ability_string =
        ability_scores_list.append(monster_json.get(ability))



def monster_reference(monster_json):
    name = monster_json.get("name") + "\n"
    size = monster_json.get("size")
    monster_type = monster_json.get("type")
    alignment = monster_json.get("alignment")
    armor_class = monster_json.get("armor_class")
    hit_points_average = monster_json.get("hit_points")
    hit_points_calculations = get_hit_points_calculation(monster_json.get("hit_dice"), monster_json.get("constitution"))
    speed = get_speed_string(monster_json.get("speed"))
    ability_scores_string = get_ability_scores_string(monster_json)
    return_string = f"*{size} {monster_type}, {alignment}*\n\n" \
                    f"Armor Class: {armor_class}\n" \
                    f"Hit Points: {hit_points_average} ({hit_points_calculations})\n" \
                    f"Speed: {speed}"
    return name, return_string
