from UtilityHandler import read_json


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
    return formatted_level_features


def class_reference(class_json):
    messages = []
    name = class_json.get("name")
    levels = get_formatted_level_features(class_json)
    class_block = f"{levels}"
    messages.append((name, class_block))
    return messages
