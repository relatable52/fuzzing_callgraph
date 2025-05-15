import json


def read_json(file_path: str):
    with open(file_path) as f:
        data = json.load(f)
    return data
