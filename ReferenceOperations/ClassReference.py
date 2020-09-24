from UtilityHandler import read_json
from math import ceil


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
    return formatted_level_features + "\n"


def get_hit_points(class_json):
    name = class_json.get("name").lower()
    hit_die_value = class_json.get("hit_die")
    hit_die = "1d" + str(hit_die_value)
    hit_die_average = ceil((1+hit_die_value)/2)
    hit_points = f"\n**Hit Dice: ** {hit_die} per {name} level\n" \
                 f"**Hit Points at 1st Level: **{hit_die_value} + your Constitution modifier\n" \
                 f"**Hit Points at Higher Levels: **{hit_die} (or {hit_die_average}) + your Constitution modifier per {name} level after 1st\n"
    return hit_points + "\n"


def class_reference(class_json):
    messages = []
    name = class_json.get("name")
    levels = get_formatted_level_features(class_json)
    hit_points = get_hit_points(class_json)
    class_block = f"{levels}" \
                  f"**Hit Points** {hit_points}"
    messages.append((name, class_block))
    return messages
