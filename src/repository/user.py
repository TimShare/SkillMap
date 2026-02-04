from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import uuid

from src.core.exceptions import NotFoundException, AlreadyExistsException
from src.database.models import User
from src.service.models import UserDTO
from src.repository.interfaces.user import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get(self, user_id: int) -> UserDTO:
        user = await self.session.get(User, user_id)
        if not user:
            raise NotFoundException(f"User with id {user_id} not found")
        return UserDTO.model_validate(user)

    async def create(self, user: UserDTO) -> int:
        db_user = User(**user.model_dump(exclude_unset=True))
        self.session.add(db_user)
        try:
            await self.session.commit()
            await self.session.refresh(db_user)
            return db_user.id
        except IntegrityError:
            await self.session.rollback()
            raise AlreadyExistsException("User with this email already exists")

    async def update(self, user_id: uuid.UUID, updates: dict) -> UserDTO:
        existing_user = await self.session.get(User, user_id)
        if not existing_user:
            raise NotFoundException(f"User not found")
        
        for key, value in updates.items():
            if hasattr(existing_user, key):
                setattr(existing_user, key, value)
        
        try:
            await self.session.commit()
            await self.session.refresh(existing_user)
            return UserDTO.model_validate(existing_user)
        except IntegrityError:
            await self.session.rollback()
            raise AlreadyExistsException("Email already in use")

    async def deactivate(self, user_id: uuid.UUID) -> None:
        user = await self.session.get(User, user_id)
        if not user:
            raise NotFoundException(f"User not found")
        
        user.is_active = False
        await self.session.commit()