import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from main import Exporter


class TestExporter(unittest.TestCase):
    def test_export_json(self):
        data = {"rooms": [{"id": 1}]}
        file = Path("test_output.json")

        Exporter.to_json(data, filename=file)

        self.assertTrue(file.exists())
        file.unlink()

    def test_export_xml(self):
        data = {"rooms": [{"id": 1, "name": "X"}]}
        file = Path("test_output.xml")

        Exporter.to_xml(data, filename=file)

        self.assertTrue(file.exists())

        tree = ET.parse(file)
        root = tree.getroot()
        self.assertEqual(root.tag, "results")

        file.unlink()


if __name__ == "__main__":
    unittest.main()
