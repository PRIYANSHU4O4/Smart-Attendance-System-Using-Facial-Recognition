import cv2
import os
import csv
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGE_DIR = os.path.join(DATA_DIR, "images")
STUDENT_FILE = os.path.join(DATA_DIR, "students.csv")


def setup_storage():
    os.makedirs(IMAGE_DIR, exist_ok=True)

    if not os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["EnrollmentID", "Name", "ImageFile"])


def is_registered(enrollment_id):
    if not os.path.exists(STUDENT_FILE):
        return False

    with open(STUDENT_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        try:
            next(reader)
        except StopIteration:
            return False

        for row in reader:
            if row and row[0] == enrollment_id:
                return True

    return False


def _capture_face(enrollment_id, name):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        return False, "Camera not accessible"

    start_time = time.time()
    captured_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.putText(
            frame,
            "Look at the camera",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )

        cv2.imshow("Enrollment", frame)

        if time.time() - start_time >= 3:
            captured_frame = frame
            break

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    if captured_frame is None:
        return False, "Face capture failed"

    image_name = f"{enrollment_id}_{name}.jpg"
    image_path = os.path.join(IMAGE_DIR, image_name)
    cv2.imwrite(image_path, captured_frame)

    with open(STUDENT_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([enrollment_id, name, image_name])

    return True, "Student registered successfully"


# ---------- CLI MODE (kept for testing) ----------
def register_student():
    setup_storage()

    enrollment_id = input("Enter Enrollment ID: ").strip()
    name = input("Enter Student Name: ").strip()

    if not enrollment_id or not name:
        print("Invalid input")
        return

    if is_registered(enrollment_id):
        print("Student already registered")
        return

    success, msg = _capture_face(enrollment_id, name)
    print(msg)


# ---------- GUI MODE (USED BY FRONTEND) ----------
def register_student_gui(enrollment_id, name):
    import cv2
    import csv
    import time

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    IMAGE_DIR = os.path.join(DATA_DIR, "images")
    STUDENT_FILE = os.path.join(DATA_DIR, "students.csv")

    os.makedirs(IMAGE_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    image_filename = f"{enrollment_id}_{name}.jpg"
    image_path = os.path.join(IMAGE_DIR, image_filename)

    # Remove old image if exists (RE-REGISTER)
    if os.path.exists(image_path):
        os.remove(image_path)

    cap = cv2.VideoCapture(0)
    time.sleep(3)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Camera capture failed")
        return

    cv2.imwrite(image_path, frame)

    # Read existing students
    rows = []
    if os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, "r", newline="") as f:
            rows = list(csv.reader(f))

    # Rewrite CSV without old record
    with open(STUDENT_FILE, "w", newline="") as f:
        writer = csv.writer(f)

        if rows:
            writer.writerow(rows[0])  # header
            for row in rows[1:]:
                if row and row[0] != enrollment_id:
                    writer.writerow(row)
        else:
            writer.writerow(["EnrollmentID", "Name", "ImageFile"])

        writer.writerow([enrollment_id, name, image_filename])

    print(f"Student re-registered successfully: {name}")
