def level_check(reference_type, message):
    print(reference_type, message.split(" ")[2])
    if reference_type == "class":
        message = message.split(" ")
        if len(message) == 3 and message[2].isdigit():
            return True
    return False


def get_name(level_json):
    name = level_json.get("index")
    name = name.capitalize()
    name = name.split("-")
    name = f"{name[0]}, {name[1]}"
    return name


def get_class_specific(level_json):
    class_specific_dictionary = {"barbarian": ["rage_count", "rage_damage"],
                                 "bard": [],
                                 "cleric": [],
                                 "druid": [],
                                 "fighter": [],
                                 "monk": []
                                 }


def get_features(level_json):
    features = level_json.get("features")
    if not features:
        return ""
    features = [feature["name"] for feature in features]
    for feature in features:
        pass
    features = "\n".join(features)
    return features


def level_reference(level_json):
    messages = []
    name = get_name(level_json)
    class_specific = get_class_speficic(level_json)
    features = get_features(level_json)
    level_block = f"{features}"
    messages.append((name, level_block))
    return messages