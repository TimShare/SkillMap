import pytest
from src.core.security import hash_password, verify_password


@pytest.mark.unit
class TestSecurity:
    """Unit tests for security functions."""
    
    @pytest.mark.parametrize("password", [
        "SecurePassword123!",
        "AnotherPass456@",
        "Complex$Pass789",
    ])
    def test_hash_password(self, password):
        """Test password hashing with multiple passwords."""
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 50  # Bcrypt hashes are long
        assert hashed.startswith("$2b$")  # Bcrypt identifier
    
    @pytest.mark.parametrize("password", [
        "SecurePassword123!",
        "Test@1234",
        "MySecretPass!",
    ])
    def test_verify_password_correct(self, password):
        """Test password verification with correct passwords."""
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) == True
    
    @pytest.mark.parametrize("password,wrong_password", [
        ("SecurePassword123!", "WrongPassword456!"),
        ("Test@1234", "Test@12345"),
        ("MySecret", "YourSecret"),
    ])
    def test_verify_password_incorrect(self, password, wrong_password):
        """Test password verification with incorrect passwords."""
        hashed = hash_password(password)
        
        assert verify_password(wrong_password, hashed) == False
    
    def test_hash_different_passwords_produce_different_hashes(self):
        """Test that different passwords produce different hashes."""
        password1 = "Password1"
        password2 = "Password2"
        
        hash1 = hash_password(password1)
        hash2 = hash_password(password2)
        
        assert hash1 != hash2
    
    def test_hash_same_password_produces_different_hashes(self):
        """Test that hashing same password twice produces different hashes (salt)."""
        password = "SamePassword123!"
        
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Different hashes due to different salts
        assert hash1 != hash2
        
        # But both verify correctly
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)
