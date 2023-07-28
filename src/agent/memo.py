import json
from typing import List, Dict

class Memo:
    def __init__(self, filename: str):
        self.filename = filename

    def read_from_file(self) -> any:
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        return data

    def write_to_file(self, data: any):
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=2)

