from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def create_jwt_token(user: dict) -> str:
    return jwt.encode(user, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

async def authenticate_user(username: str, password: str):
    # fake auth
    if username == "admin" and password == "password":
        return {"id": "1", "name": "Admin", "role": "admin"}
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        return decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
