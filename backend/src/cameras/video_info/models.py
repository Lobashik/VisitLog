# models/attendance.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, time, date
from sqlalchemy import Integer, String, Time, Date, Interval


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Attendance(Base):
    __tablename__ = "attendances"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str]
    user_name: Mapped[str]
    date: Mapped[date]
    entry_time: Mapped[time]
    exit_time: Mapped[time]
    duration_minutes: Mapped[int]
