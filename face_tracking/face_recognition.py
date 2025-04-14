import cv2
import numpy as np
import os
import torch
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
from deepface import DeepFace
from pathlib import Path
import faiss
import csv

VIDEO_PATH = "output_5s.mp4"
MODEL_PATH = "yolov8n.pt"
FACES_DIR = Path("faces")
EMBEDDINGS_PATH = "faces_embeddings.npz"
OUTPUT_VIDEO = "output_tracked_new_new.mp4"
CSV_FILENAME = "recognized_people.csv"

THRESHOLD = 1.2
EMBEDDING_DIM = 512
FACE_RECO_INTERVAL = 30

device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"{device}")


def load_or_create_embeddings():

    if os.path.exists(EMBEDDINGS_PATH):
        data = np.load(EMBEDDINGS_PATH, allow_pickle=True)
        embeddings = data["embeddings"]
        labels = data["names"]
        print(f"загружены эмбеддинги из {EMBEDDINGS_PATH}. колво лиц: {len(labels)}")
        return embeddings, labels
    else:
        all_embeddings = []
        all_labels = []

        for img_path in FACES_DIR.glob("*.JPG"):
            try:
                result = DeepFace.represent(
                    img_path=str(img_path),
                    model_name="GhostFaceNet",
                    enforce_detection=False,
                )[0]
                emb = np.array(result["embedding"])
                all_embeddings.append(emb)
                all_labels.append(img_path.stem)
            except Exception as e:
                print(f"не удалось обработать {img_path.name}: {e}")

        if not all_embeddings:
            print("в папке faces не найдено ни одного лица!")
            all_embeddings = np.empty((0, EMBEDDING_DIM), dtype=np.float32)
            all_labels = []

        else:
            all_embeddings = np.array(all_embeddings, dtype=np.float32)

        np.savez_compressed(
            EMBEDDINGS_PATH,
            embeddings=all_embeddings,
            names=np.array(all_labels, dtype=object),
        )

        print(f"сохранены эмбеддинги в {EMBEDDINGS_PATH}. колво лиц: {len(all_labels)}")
        return all_embeddings, np.array(all_labels, dtype=object)


def build_faiss_index(embeddings):

    index = faiss.IndexFlatL2(EMBEDDING_DIM)
    if embeddings.shape[0] > 0:
        index.add(embeddings)
    return index


def recognize_face(face_img, index, labels):

    try:
        result = DeepFace.represent(
            img_path=face_img, model_name="GhostFaceNet", enforce_detection=False
        )[0]
        emb = np.array(result["embedding"], dtype=np.float32).reshape(1, -1)

        if index.ntotal == 0:
            return None

        distances, neighbors = index.search(emb, k=1)
        dist = distances[0][0]
        neighbor_idx = neighbors[0][0]

        if dist < THRESHOLD:
            return labels[neighbor_idx]
    except Exception as e:
        print(f"ошибка при распознавании лица: {e}")

    return None


embeddings, labels = load_or_create_embeddings()

index = build_faiss_index(embeddings)

model = YOLO(MODEL_PATH)

tracker = DeepSort(
    max_age=30,
    n_init=3,
    nms_max_overlap=1.0,
    embedder_gpu=(device != "cpu"),
)

cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter(OUTPUT_VIDEO, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

print("Начинаем трекать...")

recognized_people_log = []
frame_count = 0
track_names_cache = {}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame_count += 1

    results = model(frame, classes=[0], verbose=False, device=device)[0]

    detections = []
    if results.boxes is not None:
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = box.conf[0].cpu().item()
            detections.append(([x1, y1, x2 - x1, y2 - y1], conf, "person"))

    tracks = tracker.update_tracks(detections, frame=frame)

    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        x1, y1, x2, y2 = map(int, track.to_ltrb())

        face_crop = frame[y1:y2, x1:x2]

        if track_id in track_names_cache:
            last_checked_frame, cached_name = track_names_cache[track_id]
            if (frame_count - last_checked_frame) < FACE_RECO_INTERVAL and cached_name:
                name = cached_name
            else:
                name = recognize_face(face_crop, index, labels)
                track_names_cache[track_id] = (frame_count, name)
        else:
            name = recognize_face(face_crop, index, labels)
            track_names_cache[track_id] = (frame_count, name)

        label = name if name else f"ID: {track_id}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
        )

        if name:
            recognized_people_log.append(
                {"frame": frame_count, "track_id": track_id, "name": name}
            )

    out.write(frame)
    cv2.imshow("face tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
print(f"видео сохранено {OUTPUT_VIDEO}")

with open(CSV_FILENAME, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["frame", "track_id", "name"])
    writer.writeheader()
    for row in recognized_people_log:
        writer.writerow(row)

print(f"список распознанных в {CSV_FILENAME}")
