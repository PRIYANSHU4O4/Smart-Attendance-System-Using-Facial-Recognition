import cv2
import face_recognition
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, "data", "images")


def load_images():
    images = []
    names = []

    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    for file in os.listdir(IMAGE_DIR):
        path = os.path.join(IMAGE_DIR, file)
        img = cv2.imread(path)

        if img is None:
            continue

        images.append(img)
        names.append(os.path.splitext(file)[0])

    return images, names


def encode_faces(images, names):
    encodings = []
    valid_names = []

    for img, name in zip(images, names):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encodes = face_recognition.face_encodings(rgb)

        if face_encodes:
            encodings.append(face_encodes[0])
            valid_names.append(name)

    return encodings, valid_names


def recognize(frame, known_encodings, known_names):
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(rgb, model="hog")
    encodings = face_recognition.face_encodings(rgb, locations)

    results = []

    for encode, loc in zip(encodings, locations):
        if not known_encodings:
            continue

        distances = face_recognition.face_distance(known_encodings, encode)
        index = distances.argmin()
        distance = distances[index]

        if distance < 0.6:
            top, right, bottom, left = loc
            results.append(
                (
                    known_names[index],
                    (top * 4, right * 4, bottom * 4, left * 4),
                )
            )

    return results
