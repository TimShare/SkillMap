import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.service.user import UserService
from src.repository.user import UserRepository
from src.service.models.user import UserDTO
from src.core.exceptions import NotFoundException, AlreadyExistsException
from src.core.security import verify_password
import uuid


@pytest.mark.unit
@pytest.mark.asyncio
class TestUserService:
    """Unit tests for UserService."""
    
    async def test_create_user_hashes_password(
        self, 
        db_session: AsyncSession,
        sample_user_data
    ):
        """Test that password is hashed when creating user."""
        repo = UserRepository(db_session)
        service = UserService(repo)
        
        user_dto = UserDTO(
            name=sample_user_data["name"],
            email=sample_user_data["email"],
            hashed_password=sample_user_data["password"],  # Plain password
            is_public=sample_user_data["is_public"]
        )
        
        user_id = await service.create_user(user_dto)
        
        # Verify user was created
        created_user = await service.get_user(user_id)
        assert created_user.id == user_id
        
        # Verify password was hashed (not equal to original)
        assert created_user.hashed_password != sample_user_data["password"]
        
        # Verify hash is valid
        assert verify_password(
            sample_user_data["password"],
            created_user.hashed_password
        )
    
    async def test_get_user(self, db_session: AsyncSession, created_user):
        """Test getting a user through service."""
        repo = UserRepository(db_session)
        service = UserService(repo)
        
        user_dto = await service.get_user(created_user.id)
        
        assert user_dto.id == created_user.id
        assert user_dto.email == created_user.email
    
    async def test_get_user_not_found(self, db_session: AsyncSession):
        """Test getting non-existent user through service."""
        repo = UserRepository(db_session)
        service = UserService(repo)
        non_existent_id = uuid.uuid4()
        
        with pytest.raises(NotFoundException):
            await service.get_user(non_existent_id)
    
    @pytest.mark.parametrize("update_data,should_hash", [
        ({"name": "Updated Name"}, False),
        ({"password": "NewPassword123!"}, True),
        ({"name": "New Name", "password": "NewPass456!"}, True),
    ])
    async def test_update_user_password_handling(
        self,
        db_session: AsyncSession,
        created_user,
        update_data,
        should_hash
    ):
        """Test update_user handles password hashing correctly."""
        repo = UserRepository(db_session)
        service = UserService(repo)
        
        original_password = created_user.hashed_password
        
        user_dto = UserDTO(
            id=created_user.id,
            name=update_data.get("name", created_user.name),
            email=created_user.email,
            hashed_password=update_data.get("password", ""),
            is_public=created_user.is_public
        )
        
        updated_user = await service.update_user(created_user.id, user_dto)
        
        if should_hash:
            # Password changed, should be hashed
            assert updated_user.hashed_password != original_password
            if "password" in update_data:
                assert verify_password(
                    update_data["password"],
                    updated_user.hashed_password
                )
        else:
            # No password change
            assert updated_user.hashed_password == original_password
    
    async def test_deactivate_user(self, db_session: AsyncSession, created_user):
        """Test deactivating user through service."""
        repo = UserRepository(db_session)
        service = UserService(repo)
        
        await service.deactivate_user(created_user.id)
        
        # Verify deactivation
        deactivated_user = await service.get_user(created_user.id)
        assert deactivated_user.is_active == False
    
    async def test_deactivate_user_not_found(self, db_session: AsyncSession):
        """Test deactivating non-existent user through service."""
        repo = UserRepository(db_session)
        service = UserService(repo)
        non_existent_id = uuid.uuid4()
        
        with pytest.raises(NotFoundException):
            await service.deactivate_user(non_existent_id)
    
    async def test_create_user_duplicate_email(
        self,
        db_session: AsyncSession,
        created_user
    ):
        """Test creating user with duplicate email through service."""
        repo = UserRepository(db_session)
        service = UserService(repo)
        
        duplicate_dto = UserDTO(
            name="Different Name",
            email=created_user.email,
            hashed_password="password123",
            is_public=True
        )
        
        with pytest.raises(AlreadyExistsException):
            await service.create_user(duplicate_dto)
