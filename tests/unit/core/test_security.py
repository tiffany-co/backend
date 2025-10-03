"""
Unit tests for the core security utilities.

These tests are completely isolated and do not require any external services like a database.
They focus on verifying the correctness of the hashing and verification functions.
"""

from app.core.security import get_hashed_value, verify_value

def test_get_hashed_value():
    """
    Tests that the get_hashed_value function returns a valid bcrypt hash.
    """
    password = "mysecretpassword"
    hashed_password = get_hashed_value(password)

    # Assert that the output is a string
    assert isinstance(hashed_password, str)

    # Assert that the hash is not the same as the original password
    assert hashed_password != password

    # A valid bcrypt hash starts with '$2b$' and is 60 characters long
    assert hashed_password.startswith("$2b$")
    assert len(hashed_password) == 60

def test_verify_value():
    """
    Tests that the verify_value function correctly validates a password against its hash.
    """
    password = "a_very_secure_password_123!"
    hashed_password = get_hashed_value(password)

    # Assert that the correct password returns True
    assert verify_value(password, hashed_password) is True

    # Assert that an incorrect password returns False
    assert verify_value("wrong_password", hashed_password) is False

    # Assert that an empty password returns False against a valid hash
    assert verify_value("", hashed_password) is False
