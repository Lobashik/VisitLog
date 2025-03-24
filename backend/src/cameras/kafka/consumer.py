import asyncio
import json

from datetime import datetime

from aiokafka import AIOKafkaConsumer
from sqlalchemy.ext.asyncio import AsyncSession

from cameras.database import get_async_session
from cameras.video_info.models import Visit


KAFKA_TOPIC = "visits"
KAFKA_BROKER = "kafka:9092"


async def save_visit(session: AsyncSession, visit_data: dict):
    visit = Visit(
        person_id=visit_data["person_id"],
        room_number=visit_data["room_nuber"],
        timestamp=datetime.fromisoformat(visit_data["timestamp"])
    )
    session.add(visit)
    await session.commit()


async def consume():
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True
    )
    
    await consumer.start()
    try:
        async for session in get_async_session():
            async for message in consumer:
                visit_data = message.value
                print(f"Получено сообщение: {visit_data}")
                await save_visit(session, visit_data)
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())