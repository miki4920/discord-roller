import pickle
import json


def read_json(item_type, item):
    api = "FileStorage/SRDJson/"
    file_path = api + item_type + ".json"
    with open(file_path) as json_file:
        data = json.load(json_file)
        for json_item in data:
            if json_item["index"] == item:
                return json_item


def read_pickle(file_name):
    pickle_file = open(file_name, "rb")
    content = pickle.load(pickle_file)
    pickle_file.close()
    return content


def write_pickle(file_name, content):
    pickle_file = open(file_name, "wb")
    pickle.dump(content, pickle_file)
    pickle_file.close()


def make_ordinal(n):
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix
