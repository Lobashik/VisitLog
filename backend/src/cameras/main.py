import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from src.auth.routers import router as auth_router
from cameras.video_info.routers import router as user_router


app = FastAPI(
    title="API",
    description="API",
    version="0.0.1",
    docs_url="/api/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Настроить под фронт
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = [user_router]

for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
