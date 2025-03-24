from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import *
from .schemas import VisitSchema


class RoomService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_room_info(self, room_number: str) -> VisitSchema:
        stmt = (
            select(Visit).where(Visit.room_number == room_number)
            .order_by(Visit.time_of_enter)
            )
        result = await self.session.execute(stmt)
        return [VisitSchema.model_validate(visit) for visit in result.scalars().all()]
