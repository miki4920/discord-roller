from UtilityHandler import make_ordinal


def get_spell_meta(spell_json):
    level = spell_json.get("level")
    school = spell_json.get("school")["name"].lower()
    ritual = spell_json.get("ritual")
    if level == 0:
        spell_meta = school + " cantrip"
    else:
        spell_meta = make_ordinal(level) + "-level " + school
    if ritual:
        spell_meta += " (ritual)"
    return spell_meta


def get_components(spell_json):
    components = " ".join(spell_json.get("components"))
    material_component = spell_json.get("material")
    if material_component:
        material_component = " (" + spell_json.get("material")[:-1] + ")"
        components += material_component
    return components + "\n"


def get_duration(spell_json):
    duration = spell_json.get("duration")
    concentration = spell_json.get("concentration")
    if concentration:
        duration = "Concentration, " + duration
    return duration + "\n\n"


def get_higher_level(spell_json):
    higher_level = spell_json.get("higher_level")
    if higher_level:
        return higher_level[0] + "\n\n"
    return ""


def get_classes(spell_json):
    classes = [class_name["name"] for class_name in spell_json.get("classes")]
    classes = ", ".join(classes)
    subclasses = [subclass_name["name"] for subclass_name in spell_json.get("subclasses")]
    if subclasses:
        subclasses = ", ".join(subclasses)
        classes = classes + "; " + subclasses
    return classes


def spell_reference(spell_json):
    messages = []
    name = spell_json.get("name") + "\n"
    description = spell_json.get("desc")[0]
    level_school = get_spell_meta(spell_json)
    spell_range = spell_json.get("range")
    components = get_components(spell_json)
    duration = get_duration(spell_json)
    casting_time = spell_json.get("casting_time")
    higher_level = get_higher_level(spell_json)
    classes = get_classes(spell_json)
    spell_block = f"_{level_school}_\n\n" \
                  f"**Casting Time:** {casting_time}\n" \
                  f"**Range:** {spell_range}\n" \
                  f"**Components:** {components}" \
                  f"**Duration:** {duration}" \
                  f"**Description**\n" \
                  f"{description}\n\n" \
                  f"**At Higher Levels.** {higher_level}" \
                  f"**Spell Lists.** {classes}"
    messages.append((name, spell_block))
    return messages
