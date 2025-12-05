import unittest
from unittest.mock import MagicMock
from main import Repository, Room, Student


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.repo = Repository(self.db)

    def test_insert_rooms(self):
        rooms = [Room(1, "A"), Room(2, "B")]

        self.repo.insert_rooms(rooms)

        self.db.executemany.assert_called_once()
        sql, params = self.db.executemany.call_args[0]
        self.assertIn("INSERT INTO rooms", sql)
        self.assertEqual(params, [(1, "A"), (2, "B")])

    def test_insert_students(self):
        students = [Student(1, "John", "2005-01-01", "M", 1)]

        self.repo.insert_students(students)

        self.db.executemany.assert_called_once()
        sql, params = self.db.executemany.call_args[0]
        self.assertIn("INSERT INTO students", sql)
        self.assertEqual(params, [(1, "John", "2005-01-01", "M", 1)])

    def test_rooms_with_student_count(self):
        self.db.execute.return_value = [{"id": 1, "student_count": 2}]
        result = self.repo.rooms_with_student_count()
        self.assertEqual(result, [{"id": 1, "student_count": 2}])


if __name__ == "__main__":
    unittest.main()
