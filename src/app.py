from fastapi import FastAPI
from src.interface.routers.user import router as user_router
from src.core import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.title,
    description="API for managing and retrieving skill maps.",
    version=settings.version,
    debug=settings.debug,
)

app.include_router(user_router)


@app.get("/ping")
async def ping():
    return {"message": "pong!"}