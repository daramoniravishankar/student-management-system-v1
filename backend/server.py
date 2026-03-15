import json
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer

# Connect to database
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    course TEXT,
    grade TEXT
)
""")

conn.commit()


class Server(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    # GET ALL STUDENTS (ALPHABETICAL ORDER)
    def do_GET(self):

        if self.path == "/students":

            cursor.execute(
                "SELECT * FROM students ORDER BY name ASC"
            )

            rows = cursor.fetchall()

            students = []

            for r in rows:
                students.append({
                    "id": r[0],
                    "name": r[1],
                    "course": r[2],
                    "grade": r[3]
                })

            self._set_headers()
            self.wfile.write(json.dumps(students).encode())

    # ADD STUDENT
    def do_POST(self):

        if self.path == "/students":

            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)

            data = json.loads(body)

            name = data["name"]
            course = data["course"]
            grade = data["grade"]

            cursor.execute(
                "INSERT INTO students(name,course,grade) VALUES (?,?,?)",
                (name, course, grade)
            )

            conn.commit()

            self._set_headers()
            self.wfile.write(json.dumps({"message": "Student Added"}).encode())

    # UPDATE STUDENT
    def do_PUT(self):

        if self.path.startswith("/students/"):

            student_id = self.path.split("/")[-1]

            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)

            data = json.loads(body)

            name = data["name"]
            course = data["course"]
            grade = data["grade"]

            cursor.execute(
                "UPDATE students SET name=?, course=?, grade=? WHERE id=?",
                (name, course, grade, student_id)
            )

            conn.commit()

            self._set_headers()
            self.wfile.write(json.dumps({"message": "Student Updated"}).encode())

    # DELETE STUDENT
    def do_DELETE(self):

        if self.path.startswith("/students/"):

            student_id = self.path.split("/")[-1]

            cursor.execute(
                "DELETE FROM students WHERE id=?",
                (student_id,)
            )

            conn.commit()

            self._set_headers()
            self.wfile.write(json.dumps({"message": "Student Deleted"}).encode())


def run():
    server_address = ("", 5000)
    httpd = HTTPServer(server_address, Server)
    print("Server running on port 5000")
    httpd.serve_forever()


run()