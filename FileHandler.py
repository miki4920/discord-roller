import pickle


def read_file(file_name):
    pickle_file = open(file_name, "rb")
    content = pickle.load(pickle_file)
    pickle_file.close()
    return content


def write_file(file_name, content):
    pickle_file = open(file_name, "wb")
    pickle.dump(content, pickle_file)
    pickle_file.close()
