import pickle
from os import path, mkdir
import requests
import json


def read_json(api, item):
    url = api + item
    response = requests.get(url)
    data = json.loads(response.text)
    return data


def read_pickle(file_name):
    pickle_file = open(file_name, "rb")
    content = pickle.load(pickle_file)
    pickle_file.close()
    return content


def write_pickle(file_name, content):
    pickle_file = open(file_name, "wb")
    pickle.dump(content, pickle_file)
    pickle_file.close()


def check_dir_existence(dir_path):
    return path.isdir(dir_path)


def make_dir(dir_path):
    mkdir(dir_path)


def make_ordinal(n):
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix
