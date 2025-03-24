from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime

from cameras.database import Base


class Room(Base):
    __tablename__ = "rooms"
    
    number: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        primary_key=True
        )
    
    visits: Mapped[list["Visit"]] = relationship(back_populates="room")


class Visit(Base):
    __tablename__ = "visits"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"), nullable=False)
    room_number: Mapped[str] = mapped_column(ForeignKey("rooms.number"), nullable=False)
    time_of_enter: Mapped[datetime] = mapped_column(DateTime)
    time_of_exit: Mapped[datetime] = mapped_column(DateTime)
    
    person: Mapped["Person"] = relationship(back_populates="visits")
    room: Mapped["Room"] = relationship(back_populates="visits")


class Person(Base):
    __tablename__ = "persons"
    
    id: Mapped[int] = mapped_column(primary_key=True)    
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
    
    visits: Mapped[list["Visit"]] = relationship(back_populates="person")
