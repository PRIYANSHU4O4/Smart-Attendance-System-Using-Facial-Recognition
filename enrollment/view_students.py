import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
STUDENT_FILE = os.path.join(DATA_DIR, "students.csv")


def get_all_students():
    students = []

    if not os.path.exists(STUDENT_FILE):
        return students

    with open(STUDENT_FILE, "r", newline="") as f:
        reader = csv.reader(f)

        # Skip header safely
        try:
            next(reader)
        except StopIteration:
            return students

        for row in reader:
            if len(row) >= 2:
                enrollment_id = row[0]
                name = row[1]
                students.append((enrollment_id, name))

    return students
