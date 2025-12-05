import unittest
from unittest.mock import patch, MagicMock
from main import App


class Args:
    rooms = "rooms.json"
    students = "students.json"
    format = "json"
    db_host = "localhost"
    db_user = "root"
    db_password = "1234"
    db_name = "schooldb"


class TestApp(unittest.TestCase):

    @patch("main.Exporter.to_json")
    @patch("main.FileLoader.load")
    @patch("main.MySQLDatabase")
    def test_app_run(self, mock_db, mock_load, mock_json):
        mock_db.return_value = MagicMock()

        # simulate rooms.json and students.json load
        mock_load.side_effect = [
            [{"id": 1, "name": "A"}],  # rooms
            [{"id": 1, "name": "Malik", "birthday": "2001-01-01", "sex": "M", "room": 1}],
        ]

        app = App(Args())
        app.run()

        self.assertEqual(mock_load.call_count, 2)      # loaded 2 files
        mock_json.assert_called_once()                 # output written
        self.assertTrue(mock_db.return_value.execute.called)  # schema/index creation


if __name__ == "__main__":
    unittest.main()
