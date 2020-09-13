def convert_stat_to_bonus(stat):
    pass


def monster_reference(monster_json):
    name = monster_json.get("name") + "\n"
    size = monster_json.get("size")
    monster_type = monster_json.get("type")
    alignment = monster_json.get("alignment")
    armor_class = monster_json.get("armor_class")
    hit_points = monster_json.get("hit_points")
    return_string = f"*{size} {monster_type}, {alignment}*\n\n" \
                    f"Armor Class {armor_class}\n" \
                    f"Hit Points {hit_points}\n"
    return name, return_string