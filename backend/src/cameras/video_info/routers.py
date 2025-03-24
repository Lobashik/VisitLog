from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from cameras.database import get_async_session
from .schemas import VisitSchema
from .services import RoomService


router = APIRouter(
    prefix="/video_info",
)


# @router.get("/room/{room_number}", response_model=list[VisitSchema])
# async def get_room(room_number: str,
#                    room_service: RoomService = Depends()):
#     response_data = await room_service.get_room_info(room_number=room_number)
#     return response_data
    
    