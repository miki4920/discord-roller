import pickle
from os import path, mkdir


def read_file(file_name):
    pickle_file = open(file_name, "rb")
    content = pickle.load(pickle_file)
    pickle_file.close()
    return content


def write_file(file_name, content):
    pickle_file = open(file_name, "wb")
    pickle.dump(content, pickle_file)
    pickle_file.close()


def check_dir_existence(dir_path):
    return path.isdir(dir_path)


def make_dir(dir_path):
    mkdir(dir_path)
