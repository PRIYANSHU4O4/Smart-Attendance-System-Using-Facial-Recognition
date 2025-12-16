import cv2
from backend.face_engine import load_images, encode_faces, recognize

images, names = load_images()
encodings, names = encode_faces(images, names)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = recognize(frame, encodings, names)

    for name, loc in results:
        y1, x2, y2, x1 = loc
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(frame, name, (x1, y2-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)

    cv2.imshow("Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
