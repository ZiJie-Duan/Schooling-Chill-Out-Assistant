import json
from typing import Any, List, Dict

class Memo:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = self.read_from_file()
    
    def __call__(self, args: str) -> Any:
        return self.data[args]

    def update(self, **kwargs: Any) -> None:
        # remove the key that is not in the data
        for key, value in kwargs.items():
            if key in self.data:
                self.data[key] = value
        self.write_to_file()

    def read_from_file(self) -> any:
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        return data

    def write_to_file(self):
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=2)

    def register(self, key: str, value: Any) -> None:
        if key not in self.data:
            self.data[key] = value
            self.write_to_file()

