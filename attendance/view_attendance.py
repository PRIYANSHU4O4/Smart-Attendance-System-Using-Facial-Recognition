import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ATTENDANCE_FILE = os.path.join(DATA_DIR, "Attendance.csv")


def get_attendance(subject=None, date=None):
    records = []

    if not os.path.exists(ATTENDANCE_FILE):
        return records

    with open(ATTENDANCE_FILE, "r", newline="") as f:
        reader = csv.reader(f)

        try:
            header = next(reader)
        except StopIteration:
            return records

        for row in reader:
            if not row:
                continue

            # -------- HANDLE BOTH OLD & NEW CSV FORMATS --------
            if len(row) == 5:
                enrollment_id, name, sub, time, d = row
            elif len(row) == 4:
                enrollment_id, name, time, d = row
                sub = "N/A"
            else:
                continue

            # -------- APPLY FILTERS --------
            if subject and sub.lower() != subject.lower():
                continue

            if date and d != date:
                continue

            records.append([enrollment_id, name, sub, time, d])

    return records
