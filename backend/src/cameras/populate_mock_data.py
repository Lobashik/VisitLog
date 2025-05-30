import asyncio
import random
from datetime import datetime, time, timedelta
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from cameras.video_info.models import Attendance, Base
from sqlalchemy.orm import sessionmaker
from faker import Faker
from cameras.config import settings
import os

# Initialize Faker for generating realistic names
fake = Faker()

# Database connection URL from environment variable
DATABASE_URL = settings.get_database_url

# Create async engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False
)

# Function to generate random time within a range
def random_time(start_hour, end_hour):
    hour = random.randint(start_hour, end_hour)
    minute = random.randint(0, 59)
    return time(hour, minute)

# Function to calculate duration in minutes between entry and exit
def calculate_duration(entry: time, exit: time) -> int:
    entry_dt = datetime.combine(datetime.today(), entry)
    exit_dt = datetime.combine(datetime.today(), exit)
    if exit_dt < entry_dt:
        exit_dt += timedelta(days=1)  # Handle overnight shifts
    duration = (exit_dt - entry_dt).seconds // 60
    return duration

# Generate mock data
async def generate_mock_data(num_records: int = 50):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Create tables if not exist

    async with AsyncSessionLocal() as session:
        for _ in range(num_records):
            # Generate random user data
            user_id = fake.uuid4()
            user_name = fake.name()
            
            # Generate random date within the last 30 days
            days_back = random.randint(0, 30)
            date = (datetime.now() - timedelta(days=days_back)).date()
            
            # Generate random entry and exit times
            entry_time = random_time(6, 12)  # Entry between 6 AM and 12 PM
            exit_time = random_time(14, 23)  # Exit between 2 PM and 11 PM
            
            # Calculate duration
            duration_minutes = calculate_duration(entry_time, exit_time)
            
            # Create attendance record
            attendance = Attendance(
                user_id=user_id,
                user_name=user_name,
                date=date,
                entry_time=entry_time,
                exit_time=exit_time,
                duration_minutes=duration_minutes
            )
            
            # Add to session
            session.add(attendance)
        
        # Commit all records
        await session.commit()
        print(f"Successfully generated {num_records} mock attendance records.")

# Run the script
if __name__ == "__main__":
    asyncio.run(generate_mock_data(50))