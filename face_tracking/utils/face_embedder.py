from deepface import DeepFace
import cv2
import numpy as np


def get_embedding(face_img):
    face_resized = cv2.resize(face_img, (160, 160))
    embedding = DeepFace.represent(
        img_path=face_resized, model_name="Facenet512", enforce_detection=False
    )[0]["embedding"]
    return np.array(embedding)


def normalize_embedding(embedding):
    norm = np.linalg.norm(embedding)
    return embedding if norm == 0 else embedding / norm
