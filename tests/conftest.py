import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient, ASGITransport
import uuid

from src.app import app
from src.database.base import Base
from src.core.database import get_session
from src.database.models.user import User

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/skillmap_test"


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session with fresh schema."""
    # Create new engine for each test to avoid event loop issues
    test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=NullPool)
    TestSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    
    # Drop and recreate tables for each test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # Create new session
    async with TestSessionLocal() as session:
        yield session
        # Cleanup
        await session.rollback()
        await session.close()
    
    # Dispose engine
    await test_engine.dispose()


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with overridden dependencies."""
    async def override_get_session():
        yield db_session
    
    app.dependency_overrides[get_session] = override_get_session
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Sample user data for tests."""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "SecurePass123!",
        "is_public": True
    }


@pytest.fixture
def sample_user_data_2():
    """Second sample user data for tests."""
    return {
        "name": "Иван Иванов",
        "email": "ivan@example.com",
        "password": "Password123!",
        "is_public": False
    }


@pytest.fixture
def sample_created_user(sample_user_data):
    """Sample user object for tests."""
    from src.core.security import hash_password
    
    return User(
        id=uuid.uuid4(),
        name=sample_user_data["name"],
        email=sample_user_data["email"],
        hashed_password=hash_password(sample_user_data["password"]),
        is_public=sample_user_data["is_public"],
        is_active=True
    )


@pytest.fixture
async def created_user(db_session: AsyncSession, sample_created_user: User) -> User:
    """Create a user in the database."""
    db_session.add(sample_created_user)
    await db_session.commit()
    await db_session.refresh(sample_created_user)
    return sample_created_user
