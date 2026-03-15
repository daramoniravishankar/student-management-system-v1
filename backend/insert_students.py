import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create table first
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
course TEXT,
grade TEXT
)
""")

students = [
('Rahul','Computer Science','A'),
('Anjali','Data Science','B'),
('Kiran','IT','A'),
('Sneha','CS','B'),
('Vikram','Cyber Security','A'),
('Pooja','Data Science','C'),
('Arjun','AI','A'),
('Meera','IT','B'),
('Rohit','CS','A'),
('Neha','Data Science','B'),
('Suresh','Cyber Security','C'),
('Divya','AI','A'),
('Manoj','IT','B'),
('Kavya','CS','A'),
('Ajay','Data Science','B')
]

cursor.executemany(
"INSERT INTO students(name,course,grade) VALUES (?,?,?)",
students
)

conn.commit()

print("15 students inserted successfully")