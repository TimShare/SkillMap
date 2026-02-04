from src.core.exceptions import NotFoundException, AlreadyExistsException
from src.core.security import hash_password
from src.service.models import UserDTO
from src.repository.interfaces.user import IUserRepository
import uuid


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: UserDTO) -> uuid.UUID:
        if not user.name or not user.email or not user.hashed_password:
            raise ValueError("name, email and password are required for user creation")
        user.hashed_password = hash_password(user.hashed_password)
        return await self.user_repository.create(user)

    async def get_user(self, user_id: uuid.UUID) -> UserDTO:
        return await self.user_repository.get(user_id)

    async def update_user(self, user_id: uuid.UUID, user: UserDTO) -> UserDTO:
        updates = user.model_dump(exclude_unset=True, exclude={"id"})
        if "hashed_password" in updates:
            if updates["hashed_password"]:
                updates["hashed_password"] = hash_password(updates["hashed_password"])
            else:
                del updates["hashed_password"]
        return await self.user_repository.update(user_id, updates)

    async def deactivate_user(self, user_id: uuid.UUID) -> None:
        await self.user_repository.deactivate(user_id)

