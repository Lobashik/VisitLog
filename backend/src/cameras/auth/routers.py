from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from cameras.auth.schemas import LoginRequest, LoginResponse, UserSearchResponse
from cameras.auth.utils import authenticate_user, create_jwt_token, get_current_user
from cameras.video_info.services import AttendanceService

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest):
    user = await authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt_token(user)
    return {"token": token, "user": user}

@router.get("/", response_model=UserSearchResponse)
async def get_users(
    query: Optional[str] = None,
    limit: int = 20,
    user=Depends(get_current_user)
):
    return await AttendanceService.search_users(query, limit)