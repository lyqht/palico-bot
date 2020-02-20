import json


def write_to_json(data, filePath):
    with open(filePath, 'w') as f:
        json.dump(data, f)


def read_json(filePath):
    with open(filePath, 'r') as f:
        items = json.load(f)
    return items
