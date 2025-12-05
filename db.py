import mysql.connector
from typing import List, Dict, Any


# Database Connection

class MySQLDatabase:
    def __init__(self, host, user, password, db):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )


    def execute(self, sql: str, params=None, fetch=False):
        cur = self.conn.cursor(dictionary=True)
        cur.execute(sql, params or [])
        if fetch:
            return cur.fetchall()
        self.conn.commit()


    def executemany(self, sql: str, params):
        cur = self.conn.cursor()
        cur.executemany(sql, params)
        self.conn.commit()



class Repository:
    def __init__(self, db: MySQLDatabase):
        self.db = db


    def create_schema(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                id INT PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                birthday DATE NOT NULL,
                sex VARCHAR(16) NOT NULL,
                room_id INT,
                FOREIGN KEY (room_id) REFERENCES rooms(id)
            )
        """)


    def insert_rooms(self, rooms):
        data = [(r.id, r.name) for r in rooms]
        self.db.executemany("""
            INSERT INTO rooms (id, name)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE name = VALUES(name)
        """, data)


    def insert_students(self, students):
        data = [(s.id, s.name, s.birthday, s.sex, s.room_id) for s in students]
        self.db.executemany("""
            INSERT INTO students (id, name, birthday, sex, room_id)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                name = VALUES(name),
                birthday = VALUES(birthday),
                sex = VALUES(sex),
                room_id = VALUES(room_id)
        """, data)

    # Required queries
    def rooms_with_student_count(self):
        return self.db.execute("""
            SELECT r.id, r.name, COUNT(s.id) AS student_count
            FROM rooms r
            LEFT JOIN students s ON r.id = s.room_id
            GROUP BY r.id, r.name
            ORDER BY student_count DESC
        """, fetch=True)


    def rooms_smallest_avg_age(self):
        return self.db.execute("""
            SELECT r.id, r.name,
                   AVG(TIMESTAMPDIFF(YEAR, s.birthday, curdate())) AS avg_age
            FROM rooms r
            JOIN students s ON r.id = s.room_id
            GROUP BY r.id, r.name
            ORDER BY avg_age ASC
            LIMIT 5
        """, fetch=True)


    def rooms_biggest_age_diff(self):
        return self.db.execute("""
            SELECT r.id, r.name, 
            MAX(TIMESTAMPDIFF(YEAR, s.birthday, curdate())) - AVG(TIMESTAMPDIFF(YEAR, s.birthday, curdate())) AS age_diff
            FROM rooms r
            JOIN students s ON r.id = s.room_id
            GROUP BY r.id, r.name
            ORDER BY age_diff DESC
            LIMIT 5
        """, fetch=True)


    def rooms_with_mixed_sex(self):
        return self.db.execute("""
            SELECT r.id, r.name
            FROM rooms r
            JOIN students s ON r.id = s.room_id
            GROUP BY r.id, r.name
            HAVING COUNT(DISTINCT s.sex) > 1
        """, fetch=True)

    # Create indexes based on room_id, birthday & sex
    def create_indexes(self):
        self.db.execute("CREATE INDEX idx_students_room ON students(room_id)")
        self.db.execute("CREATE INDEX idx_students_birthday ON students(birthday)")
        self.db.execute("CREATE INDEX idx_students_sex ON students(sex)")
