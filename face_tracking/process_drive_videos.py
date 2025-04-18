import os
import io
import glob
import subprocess
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SERVICE_ACCOUNT_FILE = "service_account.json"
DRIVE_FOLDER_ID = "1KtMg-Pkr8lE4to5vT98eIGevuAcHD8l_"
LOCAL_VIDEO_DIR = "face_tracking/videos"


def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )
    return build("drive", "v3", credentials=creds)


def download_videos_from_drive():
    os.makedirs(LOCAL_VIDEO_DIR, exist_ok=True)
    service = get_drive_service()

    query = f"'{DRIVE_FOLDER_ID}' in parents and mimeType='video/mp4' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])

    for file in files:
        file_id = file["id"]
        file_name = file["name"]
        local_path = os.path.join(LOCAL_VIDEO_DIR, file_name)

        if os.path.exists(local_path):
            print(f"Уже загружено: {file_name}")
            continue

        print(f"Скачиваем {file_name}...")
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(local_path, "wb")
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
        fh.close()
        print(f"Готово: {file_name}")


def run_face_tracking():
    video_files = glob.glob(os.path.join(LOCAL_VIDEO_DIR, "*.mp4"))
    for video in video_files:
        print(f"Обрабатываем: {os.path.basename(video)}")
        subprocess.run(["python", "face_tracking/test.py", video])


if __name__ == "__main__":
    download_videos_from_drive()
    run_face_tracking()
