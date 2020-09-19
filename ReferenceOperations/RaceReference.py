def get_ability_score_increase(race_json):
    ability_bonuses = race_json.get("ability_bonuses")
    ability_bonuses = [(ability['name'], ability['bonus']) for ability in ability_bonuses]
    for ability in ability_bonuses:
        pass
    return ""


def race_reference(race_json):
    messages = []
    name = race_json.get("name")
    ability_score_increase = get_ability_score_increase(race_json)
    age = race_json.get("age")
    size = race_json.get("size_description")
    speed = race_json.get("speed_description")
    race_block = f"**Ability Score Increase.** {ability_score_increase}" \
                 f"**Age.** {age}" \
                 f"**Size.** {size}" \
                 f"**Speed** {speed}"
    messages.append((name, race_block))
    return messages
