import json
from typing import Any, List, Dict

class Memo:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = self.read_from_file()
    
    def __call__(self, *args: Any) -> Any:
        return {arg:self.data[arg] for arg in args}

    def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            self.data[key] = value
        self.write_to_file()

    def read_from_file(self) -> any:
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {'LLM_memory':"这是一段重要的话，在2002年段子杰出生了"}
        return data

    def write_to_file(self):
        with open(self.filename, "w") as file:
            json.dump(self.data, file, indent=2)


