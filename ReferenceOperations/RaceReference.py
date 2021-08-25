from Utility.UtilityHandler import read_json_api


def get_traits(race_json):
    formatted_traits = ""
    traits = race_json.get("traits")
    for trait in traits:
        trait = read_json_api("trait", trait["index"])
        formatted_traits += f"**{trait['name']}. **"
        formatted_traits += trait["desc"][0] + "\n\n"
    return formatted_traits


def get_subraces(race_json):
    subraces = []
    race_json = race_json.get("subraces")
    for subrace in race_json:
        subrace_json = read_json_api("subrace", subrace["index"])
        name = subrace_json.get("name")
        ability_score_increase = subrace_json.get("ability_bonus_desc") + "\n\n"
        traits = get_traits(subrace_json)
        subrace_block = f"**Ability Score Increase.** {ability_score_increase}" \
                        f"{traits}"
        subraces.append((name, subrace_block))
    return subraces


def race_reference(race_json):
    messages = []
    name = race_json.get("name") + "\n"
    ability_score_increase = race_json.get("ability_bonus_desc") + "\n\n"
    age = race_json.get("age") + "\n\n"
    size = race_json.get("size_desc") + "\n\n"
    speed = race_json.get("speed_desc") + "\n\n"
    traits = get_traits(race_json)
    languages = race_json.get("language_desc")
    race_block = f"**Ability Score Increase.** {ability_score_increase}" \
                 f"**Age.** {age}" \
                 f"**Size.** {size}" \
                 f"**Speed.** {speed}" \
                 f"{traits}" \
                 f"**Languages.** {languages}"
    messages.append((name, race_block))
    if race_json.get("subraces"):
        messages.extend(get_subraces(race_json))
    return messages
