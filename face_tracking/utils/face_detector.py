from retinaface import RetinaFace


def detect_faces(frame):
    results = RetinaFace.detect_faces(frame)
    if not isinstance(results, dict):
        return []

    faces = []
    for face in results.values():
        x1, y1, x2, y2 = face["facial_area"]
        cropped = frame[y1:y2, x1:x2]
        if cropped.size > 0:
            faces.append(cropped)
    return faces
