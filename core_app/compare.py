import cv2
import numpy as np
from PIL import Image
import imagehash
import io

def extract_face(image_bytes):
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            return None

        x, y, w, h = faces[0]
        face_crop = img[y:y+h, x:x+w]

        return Image.fromarray(cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB))
    except:
        return None

def compare_faces(registered_bytes, captured_bytes, threshold=12):
    face1 = extract_face(registered_bytes)
    face2 = extract_face(captured_bytes)

    if face1 is None or face2 is None:
        return False

    face1 = face1.resize((256, 256)).convert("L")
    face2 = face2.resize((256, 256)).convert("L")

    h1 = imagehash.phash(face1)
    h2 = imagehash.phash(face2)

    diff = abs(h1 - h2)

    return diff <= threshold
