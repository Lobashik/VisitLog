import subprocess
import os
import pytz
import logging

from datetime import datetime

from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler


logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("/logs/recording_log.log", mode='a', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
load_dotenv()


RTSP_URL = os.getenv('RTSP_URL')
SERVICE_ACCOUNT_FILE = 'service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']
RECORD_DURATION = 300
TIMEZONE = pytz.timezone('Europe/Moscow')


def record_with_ffmpeg(rtsp_url, output_file, duration):
    cmd = [
        'ffmpeg',
        '-rtsp_transport', 'tcp',
        '-i', rtsp_url,
        '-t', str(duration),
        '-an',
        '-vf', "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='%{localtime}':x=10:y=10:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5",
        '-vcodec', 'libx264',
        '-preset', 'ultrafast',
        output_file
    ]
    subprocess.run(cmd)


def job():
    now = datetime.now(TIMEZONE)
    if 9 <= now.hour < 22:
        filename = f"camera_{now.strftime('%Y%m%d_%H%M%S')}.mp4"
        try:
            record_with_ffmpeg(RTSP_URL, filename, RECORD_DURATION)
        except subprocess.CalledProcessError as e:
            logging.error(f"Ошибка при записи видео: {e}")
    else:
        logging.info("Время для записи видео не наступило")


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', minutes=5)
    scheduler.start()
