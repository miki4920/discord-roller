def get_ability_score_increase(race_json):
    ability_bonuses = race_json.get("ability_bonuses")
    ability_bonuses = [(ability['name'], ability['bonus']) for ability in ability_bonuses]
    for ability in ability_bonuses:
        pass
    return ""


def get_traits(race_json):
    traits = race_json.get("traits")
    return traits


def race_reference(race_json):
    messages = []
    name = race_json.get("name") + "\n"
    ability_score_increase = get_ability_score_increase(race_json)
    age = race_json.get("age") + "\n"
    size = race_json.get("size_description") + "\n"
    speed = race_json.get("speed_description") + "\n"
    traits = get_traits(race_json)
    languages = race_json.get("language_desc")
    race_block = f"**Ability Score Increase.** {ability_score_increase}" \
                 f"**Age.** {age}" \
                 f"**Size.** {size}" \
                 f"**Speed** {speed}" \
                 f"**Traits** {traits}" \
                 f"**Languages** {languages}"
    messages.append((name, race_block))
    return messages
