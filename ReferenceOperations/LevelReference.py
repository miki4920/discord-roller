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


def level_reference(level_json):
    messages = []
    name = get_name(level_json)
    messages.append((name, level_json.get("index")))
    return messages