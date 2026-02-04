from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core import get_session
from src.repository.user import UserRepository
from src.service.user import UserService


async def get_user_service(
    session: AsyncSession = Depends(get_session),
) -> UserService:
    """Получить сервис пользователей (DI контейнер)"""
    repo = UserRepository(session)
    return UserService(repo)
