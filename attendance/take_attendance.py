import cv2
import csv
import os
from datetime import datetime

from backend.face_engine import load_images, encode_faces, recognize


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ATTENDANCE_FILE = os.path.join(DATA_DIR, "Attendance.csv")
STUDENT_FILE = os.path.join(DATA_DIR, "students.csv")


def setup_attendance_file():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["EnrollmentID", "Name", "Subject", "Time", "Date"])


def load_student_map():
    mapping = {}

    if not os.path.exists(STUDENT_FILE):
        return mapping

    with open(STUDENT_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)

        # Skip header safely
        try:
            next(reader)
        except StopIteration:
            return mapping

        for row in reader:
            # Skip empty or malformed rows
            if not row or len(row) < 3:
                continue

            enrollment_id = row[0].strip()
            name = row[1].strip()
            image_file = row[2].strip()

            if not enrollment_id or not image_file:
                continue

            key = os.path.splitext(image_file)[0]
            mapping[key] = (enrollment_id, name)

    return mapping




def load_marked_today(subject):
    marked = set()
    today = datetime.now().strftime("%d/%m/%Y")

    if not os.path.exists(ATTENDANCE_FILE):
        return marked

    with open(ATTENDANCE_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        try:
            next(reader)
        except StopIteration:
            return marked

        for row in reader:
            if row and row[2] == subject and row[4] == today:
                marked.add(row[0])

    return marked


# 🔑 FIXED FUNCTION SIGNATURE
def start_attendance(subject):
    setup_attendance_file()

    images, names = load_images()
    known_encodings, known_names = encode_faces(images, names)
    student_map = load_student_map()

    marked = load_marked_today(subject)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Camera not accessible")
        return

    print(f"Attendance started for subject: {subject}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = recognize(frame, known_encodings, known_names)

        for key, (top, right, bottom, left) in results:
            if key not in student_map:
                continue

            enrollment_id, name = student_map[key]

            if enrollment_id in marked:
                continue

            now = datetime.now()

            with open(ATTENDANCE_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    enrollment_id,
                    name,
                    subject,
                    now.strftime("%H:%M:%S"),
                    now.strftime("%d/%m/%Y"),
                ])

            marked.add(enrollment_id)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{name} ✓",
                (left, bottom - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 255),
                2,
            )

        cv2.putText(
            frame,
            f"Subject: {subject} | Press Q to Exit",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
        )

        cv2.imshow("Attendance", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Attendance session ended")
