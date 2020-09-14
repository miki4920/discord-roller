from math import floor


def ability_conversion(ability_score):
    ability_score = str(floor(int(ability_score) / 2) - 5)
    if int(ability_score) > 0:
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
    for proficiency in proficiencies:
        if "Saving Throw" in proficiency["name"]:
            value = proficiency['value']
            if value > 0:
                value = "+" + str(value)
            saving_throws.append(f"{proficiency['name'][-3:]}: {proficiency['value']}")
    print(saving_throws)
    return "Saving Throws: " + " ".join(saving_throws) + "\n"


def monster_reference(monster_json):
    name = monster_json.get("name") + "\n"
    size = monster_json.get("size")
    monster_type = monster_json.get("type")
    alignment = monster_json.get("alignment") + "*\n\n"
    armor_class = str(monster_json.get("armor_class")) + "\n"
    hit_points_average = str(monster_json.get("hit_points"))
    hit_points_calculations = "(" + str(get_hit_points_calculation(monster_json.get("hit_dice"), monster_json.get("constitution"))) + ")\n"
    speed = get_speed(monster_json.get("speed"))
    ability_scores_string = get_ability_scores(monster_json)
    proficiencies = monster_json.get("proficiencies")
    if proficiencies:
        proficiencies = get_proficiencies(proficiencies) + "\n"
    return_string = f"*{size} {monster_type}, {alignment}" \
                    f"Armor Class: {armor_class}" \
                    f"Hit Points: {hit_points_average} {hit_points_calculations}" \
                    f"Speed: {speed}" \
                    f"{ability_scores_string}" \
                    f"{proficiencies}"
    return name, return_string
