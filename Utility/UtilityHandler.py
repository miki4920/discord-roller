import json


def read_json(file_name):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
        return data


def read_json_api(item_type, item):
    api = "FileStorage/SRDJson/"
    file_path = api + item_type + ".json"
    with open(file_path) as json_file:
        data = json.load(json_file)
        for json_item in data:
            if json_item["index"] == item:
                return json_item


def make_ordinal(n):
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix


def escape(string):
    """Escapes formatting characters in the response"""
    escaped_string = string.replace("*", "\\*")
    return escaped_string
