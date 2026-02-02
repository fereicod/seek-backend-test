"""Unit tests for security module using pytest style with fixtures and mocks."""
import pytest
from unittest.mock import patch
from jwt import decode

from app.core.security import create_access_token


@pytest.mark.parametrize("subject,claims", [
    ("user@test.com", {}),
    ("admin@test.com", {"permissions": ["book:read", "book:create"]}),
    ("editor@test.com", {"permissions": ["book:read"], "role": "editor"}),
])
@patch("app.core.security.settings")
def test_create_token_payload(mock_settings, mock_jwt_settings, subject, claims):
    """Token should contain subject, claims and expiration."""
    mock_settings.JWT_SECRET_KEY = mock_jwt_settings.JWT_SECRET_KEY
    mock_settings.JWT_ALGORITHM = mock_jwt_settings.JWT_ALGORITHM
    mock_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES = mock_jwt_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

    token = create_access_token(subject=subject, claims=claims)
    payload = decode(token, mock_jwt_settings.JWT_SECRET_KEY, algorithms=[mock_jwt_settings.JWT_ALGORITHM])

    assert payload["sub"] == subject
    assert "exp" in payload
    for key, value in claims.items():
        assert payload[key] == value
