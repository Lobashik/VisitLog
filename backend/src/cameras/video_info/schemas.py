from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Room(BaseModel):
    number: str


class VisitCreate(BaseModel):
    person_id: int
    room_number: str


class PersonCreate(BaseModel):
    first_name: str
    last_name: str


class PersonBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    first_name: str
    last_name: str


class VisitBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    time_of_enter: datetime
    time_of_exit: datetime
    room_number: Room


class VisitSchema(VisitBase):    
    person: PersonBase


class Person(PersonBase):
    visits: list[VisitBase]
