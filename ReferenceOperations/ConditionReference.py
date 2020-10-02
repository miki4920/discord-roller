def condition_reference(condition_json):
    messages = []
    name = condition_json.get("name")
    condition_block = "\n\n".join(condition_json.get("desc"))
    messages.append((name, condition_block))
    return messages
