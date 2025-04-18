from datetime import datetime, date, time
from pydantic import BaseModel
from typing import Optional, List, Literal

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginUser(BaseModel):
    id: str
    name: str
    role: str

class LoginResponse(BaseModel):
    token: str
    user: LoginUser