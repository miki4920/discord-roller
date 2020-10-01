def level_check(reference_type, message):
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
    class_specific_block = ""
    class_specific = level_json.get("class_specific")
    if class_specific:
        for feature in class_specific:
            text_feature = feature.capitalize().replace("_", " ")
            class_specific_block += f"{text_feature}: {class_specific[feature]}\n"
    if class_specific_block:
        class_specific_block = "\n" + class_specific_block + "\n"
    return class_specific_block


def get_spell_slots(level_json):
    pass


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
    class_specific = get_class_specific(level_json)
    features = get_features(level_json)
    level_block = f"**Class Specific Features** {class_specific}" \
                  f"{features}" \
                  f""
    messages.append((name, level_block))
    return messages