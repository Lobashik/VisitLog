import pandas as pd
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from datetime import datetime, time, date, timedelta
from cameras.video_info.models import Attendance, Base  # Предполагается, что модели определены в файле models.py
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def process_attendance(csv_file_path: str, database_url: str):
    try:
        # Чтение CSV файла
        logger.info(f"Reading CSV file: {csv_file_path}")
        df = pd.read_csv(csv_file_path)
        
        # Базовая дата и время (9:00 MSK, 13 мая 2025)
        base_datetime = datetime(2025, 5, 13, 13, 0)
        
        # Преобразование timestamp в timedelta и добавление к базовой дате
        df['full_datetime'] = pd.to_timedelta(df['timestamp']) + base_datetime
        
        # Создание движка базы данных
        engine = create_async_engine(database_url, echo=True)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # Создание фабрики сессий
        async_session = async_sessionmaker(
            engine, expire_on_commit=False, class_=AsyncSession
        )
        
        async with async_session() as session:
            async with session.begin():
                # Группировка данных по track_id и name
                grouped = df.groupby(['track_id', 'name'])
                
                for (track_id, name), group in grouped:
                    # Получение времени входа (первое появление)
                    entry_datetime = group['full_datetime'].min()
                    entry_time = entry_datetime.time()
                    
                    # Получение времени выхода (последнее появление)
                    exit_datetime = group['full_datetime'].max()
                    exit_time = exit_datetime.time()
                    
                    # Вычисление длительности в минутах
                    duration = (exit_datetime - entry_datetime).total_seconds() / 60
                    
                    # Получение даты
                    attendance_date = entry_datetime.date()
                    
                    # Создание записи посещаемости
                    attendance = Attendance(
                        user_id=str(track_id),
                        user_name=name,
                        date=attendance_date,
                        entry_time=entry_time,
                        exit_time=exit_time,
                        duration_minutes=int(duration)
                    )
                    
                    session.add(attendance)
                    logger.info(f"Added attendance for {name} (ID: {track_id})")
                
                # Коммит изменений
                await session.commit()
                logger.info("All attendance records have been saved successfully")
                
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise
    finally:
        # Закрытие соединения с базой данных
        if 'engine' in locals():
            await engine.dispose()

async def main():
    # Пример использования
    csv_file_path = "data/yolo_11_retinaface.csv"
    from cameras.config import settings
    database_url = settings.get_database_url
    await process_attendance(csv_file_path, database_url)

if __name__ == "__main__":
    asyncio.run(main())