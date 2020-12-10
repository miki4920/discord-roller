from UtilityHandler import read_json
from ErrorHandler import too_high_level


def level_check(reference_type, message):
    if reference_type == "class":
        message = message.split(" ")
        if len(message) == 3 and message[2].lstrip("-").isdigit():
            if int(message[2]) > 20 or int(message[2]) < 1:
                raise too_high_level()
            return True
    return False


def get_name(level_json):
    name = level_json.get("index")
    name = name.capitalize()
    name = name.split("-")
    name = f"{name[0]}, {name[1]}"
    return name


def get_class_specific(level_json):
    class_specific_block = ""
    class_specific = level_json.get("class_specific")
    if class_specific:
        for feature in class_specific:
            text_feature = feature.capitalize().replace("_", " ")
            class_specific_block += f"{text_feature}: {class_specific[feature]}\n"
    if class_specific_block:
        class_specific_block = "**Class Specific Features**" + "\n" + class_specific_block + "\n"
    return class_specific_block


def get_spell_slots(level_json):
    spells = level_json.get("spellcasting")
    spells_block = ""
    if spells:
        count = 1
        for spell in spells:
            text_feature = spell.capitalize().replace("_", " ")
            spells_block += f"{text_feature}: {spells[spell]} "
            count += 1
            if count % 3 == 0:
                spells_block += "\n"
                if count == 3:
                    spells_block += "\n"
        spells_block = "**Spellcasting**\n" + "```" + spells_block + "```"
        spells_block += "\n"
    return spells_block


def get_features(level_json):
    features = level_json.get("features")
    features_block = ""
    if features:
        for feature in features:
            feature_json = read_json("feature", feature["index"])
            features_block += f"**{feature['name']}**\n{feature_json['desc'][0]}\n"
    return features_block


def level_reference(level_json):
    messages = []
    name = get_name(level_json)
    spells = get_spell_slots(level_json)
    class_specific = get_class_specific(level_json)
    features = get_features(level_json)
    level_block = f"{spells}" \
                  f"{class_specific}" \
                  f"{features}" \
                  f""
    messages.append((name, level_block))
    return messages
