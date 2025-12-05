# 📘 Student–Room Database Loader

A Python application that loads **rooms** and **students** from CSV/JSON files, writes them to a **MySQL** database, performs required **analytics queries**, and exports results in **JSON or XML** format.

The project follows **OOP principles**, respects **SOLID**, and avoids ORM (pure SQL only).

---

## 📌 Problem Statement

You are given two data files:

- **rooms** — list of rooms  
- **students** — list of students (many students → one room)  

Your task is to:

### ✅ 1. Create a relational database schema

Using MySQL (or PostgreSQL), build tables:

- `rooms`
- `students` with foreign key `room_id → rooms.id`

This represents a **many-to-one** relationship (many students in one room).

---

### ✅ 2. Load data from input files

The script must:

- Accept `.json` or `.csv` files  
- Parse them  
- Insert data into MySQL using SQL (NO ORM)

---

### ✅ 3. Perform required database queries

All calculations must happen on the **database level**, not in Python.

The required queries:

1. **List of rooms with number of students**  
2. **Top 5 rooms with the smallest average age**  
3. **Top 5 rooms with the biggest difference between max age and average age**  
4. **List of rooms containing students of different sexes**

These queries must use SQL functions such as:

- `COUNT`  
- `AVG`  
- `MAX`  
- `TIMESTAMPDIFF`

---


**### ✅ 4. Running the project**
  >python main.py --students students.json --rooms rooms.json --format json --db-name taskdb
!(screenshots/1.png)
<br>
### Tests
All of our tests run successfully as we can see below
!(screenshots/2.png)
<br>
### A glimples on MySQL
!(screenshots/3.png)
As we can see above our tables have been created in **testdb**, as well as indexes on students.



