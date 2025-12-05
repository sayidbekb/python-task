import csv
import json
from typing import List, Dict, Any


# Model

class Room:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Student:
    def __init__(self, id: int, name: str, birthday: str, sex: str, room_id: int):
        self.id = id
        self.name = name
        self.birthday = birthday
        self.sex = sex
        self.room_id = room_id


# File Loader

class FileLoader:
    @staticmethod
    def load(path: str) -> List[Dict[str, Any]]:
        if path.endswith(".json"):
            with open(path, "r", encoding="utf8") as f:
                return json.load(f)

        elif path.endswith(".csv"):
            with open(path, "r", encoding="utf8") as f:
                reader = csv.DictReader(f)
                return list(reader)

        else:
            raise ValueError("Only .json or .csv files are supported")
