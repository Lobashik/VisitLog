import csv
from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from cameras.video_info.models import Room, Visit, Person
from cameras.database import async_session_maker


def parse_video_filename(video: str) -> str:
    return video.removeprefix("cam_").removesuffix(".mp4")


def frame_to_datetime(frame: int, fps: int = 30) -> datetime:
    return datetime(2024, 1, 1) + timedelta(seconds=frame / fps)


def parse_people(people_str: str) -> list[str]:
    return people_str.split(";") if people_str else []


def split_name(login: str) -> tuple[str, str]:
    # Пример: ikmityushkin → I.K. Mityushkin
    if len(login) < 2:
        return "Unknown", login
    return login[1:], login[:1].upper() + login[2:]


async def get_or_create_person(session: AsyncSession, login: str) -> Person:
    last_name, first_initial = split_name(login)
    stmt = select(Person).where(Person.first_name == first_initial, Person.last_name == last_name)
    result = await session.execute(stmt)
    person = result.scalars().first()
    if person is None:
        person = Person(first_name=first_initial, last_name=last_name)
        session.add(person)
        await session.flush()
    return person


async def get_or_create_room(session: AsyncSession, room_number: str) -> Room:
    stmt = select(Room).where(Room.number == room_number)
    result = await session.execute(stmt)
    room = result.scalars().first()
    if room is None:
        room = Room(number=room_number)
        session.add(room)
        await session.flush()
    return room


async def process_csv(file_path: str):
    async with async_session_maker() as session:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            last_seen: dict[tuple[int, str], Visit] = {}

            for row in reader:
                video = row["video"]
                frame = int(row["frame"])
                people = parse_people(row["people"])

                room_number = parse_video_filename(video)
                timestamp = frame_to_datetime(frame)

                room = await get_or_create_room(session, room_number)

                for login in people:
                    person = await get_or_create_person(session, login)

                    key = (person.id, room.number)

                    if key in last_seen:
                        # обновим время выхода
                        last_seen[key].time_of_exit = timestamp
                    else:
                        visit = Visit(
                            person_id=person.id,
                            room_number=room.number,
                            time_of_enter=timestamp,
                            time_of_exit=timestamp
                        )
                        session.add(visit)
                        last_seen[key] = visit

            await session.commit()
