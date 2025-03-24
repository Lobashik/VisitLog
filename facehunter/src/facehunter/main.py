import cv2
import os

def extract_faces(video_path, output_dir="faces", frame_step=10):
    os.makedirs(output_dir, exist_ok=True)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    video = cv2.VideoCapture(video_path)
    
    frame_count = 0
    while True:
        success, frame = video.read()
        if not success:
            break

        if frame_count % frame_step == 0:  # Обрабатываем каждый N-й кадр
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            for i, (x, y, w, h) in enumerate(faces):
                face = frame[y:y+h, x:x+w]
                face_path = f"{output_dir}/face_{frame_count}_{i}.jpg"
                cv2.imwrite(face_path, face)

        frame_count += 1

    video.release()
    print(f"Извлечение лиц завершено. Лица сохранены в папке {output_dir}")

# Использование
video_file = "test_video.mp4"  # Укажи путь к видео
extract_faces(video_file)
