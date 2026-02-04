from abc import ABC, abstractmethod
from src.service.models.user import UserDTO
import uuid

class IUserRepository(ABC):
    @abstractmethod
    def get(self, user_id: uuid.UUID) -> UserDTO:
        pass
    
    @abstractmethod
    def create(self, user: UserDTO) -> uuid.UUID:
        pass

    @abstractmethod
    def update(self, user: UserDTO) -> None:
        pass

    @abstractmethod
    def deactivate(self, user: UserDTO) -> None:
        pass