import pytest
from httpx import AsyncClient
from syrupy.assertion import SnapshotAssertion
import uuid


@pytest.mark.integration
@pytest.mark.asyncio
class TestUserAPI:
    """Integration tests for User API endpoints with snapshot testing."""
    
    async def test_create_user_success(
        self,
        client: AsyncClient,
        sample_user_data,
        snapshot: SnapshotAssertion
    ):
        """Test creating a new user."""
        response = await client.post("/users/", json=sample_user_data)
        
        assert response.status_code == 201
        data = response.json()
        
        # Validate UUID
        assert "id" in data
        assert uuid.UUID(data["id"])
        
        # Canonize response (excluding dynamic UUID)
        snapshot_data = {k: v for k, v in data.items() if k != "id"}
        snapshot.assert_match(snapshot_data)
    
    async def test_create_user_duplicate_email(
        self,
        client: AsyncClient,
        created_user,
        sample_user_data,
        snapshot: SnapshotAssertion
    ):
        """Test creating user with duplicate email."""
        response = await client.post("/users/", json=sample_user_data)
        
        assert response.status_code == 409
        snapshot.assert_match(response.json())
    
    @pytest.mark.parametrize("invalid_data,expected_status", [
        (
            {"name": "Test", "email": "not-an-email", "password": "Pass123!"},
            422
        ),
        (
            {"name": "Test", "email": "test@example.com"},  # Missing password
            422
        ),
        (
            {"email": "test@example.com", "password": "Pass123!"},  # Missing name
            422
        ),
    ])
    async def test_create_user_validation_errors(
        self,
        client: AsyncClient,
        invalid_data,
        expected_status,
        snapshot: SnapshotAssertion
    ):
        """Test creating user with various validation errors."""
        response = await client.post("/users/", json=invalid_data)
        
        assert response.status_code == expected_status
        snapshot.assert_match(response.json())
    
    async def test_get_user_success(
        self,
        client: AsyncClient,
        created_user,
        snapshot: SnapshotAssertion
    ):
        """Test getting an existing user."""
        response = await client.get(f"/users/{created_user.id}")
        
        assert response.status_code == 200
        data = response.json()
        
        # Validate UUID
        assert data["id"] == str(created_user.id)
        
        # Canonize response
        snapshot_data = {k: v for k, v in data.items() if k != "id"}
        snapshot.assert_match(snapshot_data)
    
    async def test_get_user_not_found(
        self,
        client: AsyncClient,
        snapshot: SnapshotAssertion
    ):
        """Test getting a non-existent user."""
        non_existent_id = uuid.uuid4()
        response = await client.get(f"/users/{non_existent_id}")
        
        assert response.status_code == 404
        # Remove UUID from error message for consistent snapshot
        data = response.json()
        if "detail" in data and str(non_existent_id) in data["detail"]:
            data["detail"] = data["detail"].replace(str(non_existent_id), "<UUID>")
        snapshot.assert_match(data)
    
    async def test_get_user_invalid_uuid(
        self,
        client: AsyncClient,
        snapshot: SnapshotAssertion
    ):
        """Test getting user with invalid UUID format."""
        response = await client.get("/users/not-a-uuid")
        
        assert response.status_code == 422
        snapshot.assert_match(response.json())
    
    @pytest.mark.parametrize("update_data", [
        {"name": "Updated Name"},
        {"is_public": False},
        {"name": "New Name", "is_public": False},
    ])
    async def test_update_user_success(
        self,
        client: AsyncClient,
        created_user,
        update_data,
        snapshot: SnapshotAssertion
    ):
        """Test updating user with different field combinations."""
        response = await client.put(
            f"/users/{created_user.id}",
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify updates
        for field, value in update_data.items():
            assert data[field] == value
        
        # Canonize response
        snapshot_data = {k: v for k, v in data.items() if k != "id"}
        snapshot.assert_match(snapshot_data)
    
    async def test_update_user_password(
        self,
        client: AsyncClient,
        created_user,
        snapshot: SnapshotAssertion
    ):
        """Test updating user password."""
        update_data = {"password": "NewSecurePass456!"}
        response = await client.put(
            f"/users/{created_user.id}",
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Password should not be in response
        assert "password" not in data
        assert "hashed_password" not in data
        
        snapshot_data = {k: v for k, v in data.items() if k != "id"}
        snapshot.assert_match(snapshot_data)
    
    async def test_update_user_not_found(
        self,
        client: AsyncClient,
        snapshot: SnapshotAssertion
    ):
        """Test updating a non-existent user."""
        non_existent_id = uuid.uuid4()
        update_data = {"name": "New Name"}
        
        response = await client.put(
            f"/users/{non_existent_id}",
            json=update_data
        )
        
        assert response.status_code == 404
        snapshot.assert_match(response.json())
    
    @pytest.mark.parametrize("invalid_email", [
        "not-an-email",
        "missing-at-sign.com",
        "@no-local-part.com",
    ])
    async def test_update_user_invalid_email(
        self,
        client: AsyncClient,
        created_user,
        invalid_email,
        snapshot: SnapshotAssertion
    ):
        """Test updating user with various invalid emails."""
        update_data = {"email": invalid_email}
        response = await client.put(
            f"/users/{created_user.id}",
            json=update_data
        )
        
        assert response.status_code == 422
        snapshot.assert_match(response.json())
    
    async def test_delete_user_success(
        self,
        client: AsyncClient,
        created_user
    ):
        """Test deactivating a user."""
        response = await client.delete(f"/users/{created_user.id}")
        
        assert response.status_code == 204
        assert response.text == ""
        
        # Verify user is deactivated
        get_response = await client.get(f"/users/{created_user.id}")
        assert get_response.status_code == 200
        assert get_response.json()["is_active"] == False
    
    async def test_delete_user_not_found(
        self,
        client: AsyncClient,
        snapshot: SnapshotAssertion
    ):
        """Test deactivating a non-existent user."""
        non_existent_id = uuid.uuid4()
        response = await client.delete(f"/users/{non_existent_id}")
        
        assert response.status_code == 404
        snapshot.assert_match(response.json())
    
    async def test_create_multiple_users(
        self,
        client: AsyncClient,
        sample_user_data,
        sample_user_data_2,
        snapshot: SnapshotAssertion
    ):
        """Test creating multiple users."""
        # Create first user
        response1 = await client.post("/users/", json=sample_user_data)
        assert response1.status_code == 201
        user1 = response1.json()
        
        # Create second user
        response2 = await client.post("/users/", json=sample_user_data_2)
        assert response2.status_code == 201
        user2 = response2.json()
        
        # Verify different IDs
        assert user1["id"] != user2["id"]
        
        # Canonize responses
        users_snapshot = [
            {k: v for k, v in user1.items() if k != "id"},
            {k: v for k, v in user2.items() if k != "id"}
        ]
        snapshot.assert_match(users_snapshot)
    
    async def test_full_user_lifecycle(
        self,
        client: AsyncClient,
        sample_user_data,
        snapshot: SnapshotAssertion
    ):
        """Test complete user lifecycle: create, get, update, deactivate."""
        # 1. Create user
        create_response = await client.post("/users/", json=sample_user_data)
        assert create_response.status_code == 201
        user_id = create_response.json()["id"]
        
        # 2. Get user
        get_response = await client.get(f"/users/{user_id}")
        assert get_response.status_code == 200
        assert get_response.json()["is_active"] == True
        
        # 3. Update user
        update_data = {"name": "Updated Name", "is_public": False}
        update_response = await client.put(f"/users/{user_id}", json=update_data)
        assert update_response.status_code == 200
        updated_user = update_response.json()
        assert updated_user["name"] == "Updated Name"
        
        # 4. Deactivate user
        delete_response = await client.delete(f"/users/{user_id}")
        assert delete_response.status_code == 204
        
        # 5. Verify deactivation
        final_response = await client.get(f"/users/{user_id}")
        assert final_response.status_code == 200
        final_user = final_response.json()
        assert final_user["is_active"] == False
        
        # Canonize lifecycle data
        lifecycle_snapshot = {
            "created": {k: v for k, v in create_response.json().items() if k != "id"},
            "updated": {k: v for k, v in updated_user.items() if k != "id"},
            "deactivated": {k: v for k, v in final_user.items() if k != "id"}
        }
        snapshot.assert_match(lifecycle_snapshot)
