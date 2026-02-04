import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.user import UserRepository
from src.service.models.user import UserDTO
from src.core.exceptions import NotFoundException, AlreadyExistsException
import uuid


@pytest.mark.unit
@pytest.mark.asyncio
class TestUserRepository:
    """Unit tests for UserRepository."""
    
    async def test_create_user(self, db_session: AsyncSession, sample_user_data):
        """Test creating a new user."""
        repo = UserRepository(db_session)
        user_dto = UserDTO(
            name=sample_user_data["name"],
            email=sample_user_data["email"],
            hashed_password="hashed_password_123",
            is_public=sample_user_data["is_public"]
        )
        
        user_id = await repo.create(user_dto)
        
        assert user_id is not None
        assert isinstance(user_id, uuid.UUID)
    
    async def test_get_user_success(self, db_session: AsyncSession, created_user):
        """Test getting an existing user."""
        repo = UserRepository(db_session)
        
        user_dto = await repo.get(created_user.id)
        
        assert user_dto.id == created_user.id
        assert user_dto.name == created_user.name
        assert user_dto.email == created_user.email
        assert user_dto.is_active == True
    
    async def test_get_user_not_found(self, db_session: AsyncSession):
        """Test getting a non-existent user."""
        repo = UserRepository(db_session)
        non_existent_id = uuid.uuid4()
        
        with pytest.raises(NotFoundException) as exc_info:
            await repo.get(non_existent_id)
        
        assert "not found" in str(exc_info.value.message).lower()
    
    async def test_create_user_duplicate_email(
        self,
        db_session: AsyncSession,
        created_user
    ):
        """Test creating user with duplicate email raises exception."""
        repo = UserRepository(db_session)
        duplicate_dto = UserDTO(
            name="Different Name",
            email=created_user.email,  # Same email
            hashed_password="hashed_password_456",
            is_public=True
        )
        
        with pytest.raises(AlreadyExistsException) as exc_info:
            await repo.create(duplicate_dto)
        
        assert "email" in str(exc_info.value.message).lower()
    
    @pytest.mark.parametrize("update_fields", [
        {"name": "Updated Name"},
        {"is_public": False},
        {"name": "New Name", "is_public": False},
    ])
    async def test_update_user(
        self,
        db_session: AsyncSession,
        created_user,
        update_fields
    ):
        """Test updating user with different field combinations."""
        repo = UserRepository(db_session)
        
        updated_dto = await repo.update(created_user.id, update_fields)
        
        assert updated_dto.id == created_user.id
        for field, value in update_fields.items():
            assert getattr(updated_dto, field) == value
    
    async def test_update_user_not_found(self, db_session: AsyncSession):
        """Test updating non-existent user raises exception."""
        repo = UserRepository(db_session)
        non_existent_id = uuid.uuid4()
        
        with pytest.raises(NotFoundException):
            await repo.update(non_existent_id, {"name": "New Name"})
    
    async def test_deactivate_user(self, db_session: AsyncSession, created_user):
        """Test deactivating a user."""
        repo = UserRepository(db_session)
        
        await repo.deactivate(created_user.id)
        
        # Verify user is deactivated
        deactivated_user = await repo.get(created_user.id)
        assert deactivated_user.is_active == False
    
    async def test_deactivate_user_not_found(self, db_session: AsyncSession):
        """Test deactivating non-existent user raises exception."""
        repo = UserRepository(db_session)
        non_existent_id = uuid.uuid4()
        
        with pytest.raises(NotFoundException):
            await repo.deactivate(non_existent_id)
