import argparse
import json
import xml.etree.ElementTree as ET

from db import MySQLDatabase, Repository
from models import Room, Student, FileLoader



class Exporter:
    @staticmethod
    def to_json(data, filename="result.json"):
        with open(filename, "w", encoding="utf8") as f:
            json.dump(data, f, indent=4, default=float)

    @staticmethod
    def to_xml(data, filename="result.xml"):
        root = ET.Element("results")
        for key, items in data.items():
            block = ET.SubElement(root, key)
            for item in items:
                entry = ET.SubElement(block, "item")
                for k, v in item.items():
                    elem = ET.SubElement(entry, k)
                    elem.text = str(v)
        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf8")



class App:
    def __init__(self, args):
        self.args = args
        self.db = MySQLDatabase(
            host=args.db_host,
            user=args.db_user,
            password=args.db_password,
            db=args.db_name
        )
        self.repo = Repository(self.db)


    def run(self):
        self.repo.create_schema()

        rooms_raw = FileLoader.load(self.args.rooms)
        students_raw = FileLoader.load(self.args.students)

        rooms = [Room(int(r["id"]), r["name"]) for r in rooms_raw]
        students = [
            Student(int(s["id"]), s["name"], s["birthday"][:10], s["sex"], int(s["room"]))
            for s in students_raw
        ]

        self.repo.insert_rooms(rooms)
        self.repo.insert_students(students)

        result = {
            "rooms_with_student_count": self.repo.rooms_with_student_count(),
            "rooms_smallest_avg_age": self.repo.rooms_smallest_avg_age(),
            "rooms_biggest_age_diff": self.repo.rooms_biggest_age_diff(),
            "rooms_with_mixed_sex": self.repo.rooms_with_mixed_sex()
        }

        self.repo.create_indexes()

        if self.args.format == "json":
            Exporter.to_json(result)
            print("Saved to result.json")
        else:
            Exporter.to_xml(result)
            print("Saved to result.xml")


# CLI Interface

def cli():
    parser = argparse.ArgumentParser()

    parser.add_argument("--students", required=True)
    parser.add_argument("--rooms", required=True)
    parser.add_argument("--format", choices=["json", "xml"], required=True)

    parser.add_argument("--db-host", default="localhost")
    parser.add_argument("--db-user", default="root")
    parser.add_argument("--db-password", default="1234")
    parser.add_argument("--db-name", default="newschooldb")

    return parser.parse_args()


if __name__ == "__main__":
    args = cli()
    App(args).run()
