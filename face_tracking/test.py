import os
import cv2
import numpy as np
from pathlib import Path
from utils.face_detector import detect_faces
from utils.face_embedder import get_embedding, normalize_embedding
from utils.searcher import FaceSearcher
import csv

BASE_DIR = Path(__file__).resolve().parent
video_dir = BASE_DIR / "videos"
embeddings_path = BASE_DIR / "embeddings_Facenet512.npz"

frame_step = 30
threshold = 1.04

allowed_names = {
    "masadkovskaya",
    "aimilovanova",
    "avvorobev",
    "mapivovarova",
    "ikmityushkin",
    "aaivoninskaya",
}

searcher = FaceSearcher(embeddings_path)

with open("recognition_log.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["video", "frame", "detect", "people"])

    for video_file in os.listdir(video_dir):
        if not video_file.endswith(".mp4"):
            continue

        cap = cv2.VideoCapture(str(video_dir / video_file))
        frame_num = 0
        print(f"\nвидео: {video_file}")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_num += 1
            if frame_num % frame_step != 0:
                continue

            faces = detect_faces(frame)
            people = []

            for face_crop in faces:
                try:
                    emb = get_embedding(face_crop)
                    emb = normalize_embedding(emb.reshape(1, -1).astype("float32"))
                    label, dist = searcher.search(emb)
                    name = label.split("_")[0]
                    if dist < threshold and name in allowed_names:
                        people.append(name)
                except Exception as e:
                    print(f"[Warning] ошибка распознавания: {e}")

            people = list(set(people))
            print(
                f"frame: {frame_num}, detect: {len(faces)}, people: {', '.join(people) if people else 'None'}"
            )
            writer.writerow([video_file, frame_num, len(faces), ";".join(people)])

        cap.release()
