import unittest
import tempfile
import json
import csv
from main import FileLoader


class TestFileLoader(unittest.TestCase):
    def test_load_json(self):
        data = [{"id": 1, "name": "Room A"}]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            path = f.name

        loaded = FileLoader.load(path)
        self.assertEqual(loaded, data)

    def test_load_csv(self):
        rows = [
            {"id": "1", "name": "Room A"},
            {"id": "2", "name": "Room B"},
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=["id", "name"])
            writer.writeheader()
            writer.writerows(rows)
            path = f.name

        loaded = FileLoader.load(path)
        self.assertEqual(loaded, rows)

    def test_load_invalid(self):
        with tempfile.NamedTemporaryFile(suffix=".txt") as f:
            with self.assertRaises(ValueError):
                FileLoader.load(f.name)


if __name__ == "__main__":
    unittest.main()
