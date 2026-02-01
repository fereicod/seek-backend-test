"""
Pytest configuration and shared fixtures.
Environment variables are loaded from .env.test via pytest-dotenv
"""
import pytest
from unittest.mock import MagicMock
from datetime import datetime
from bson import ObjectId


@pytest.fixture
def mock_jwt_settings():
    """Mock JWT settings to avoid using real secrets."""
    return MagicMock(
        JWT_SECRET_KEY="test_secret_key_for_testing",
        JWT_ALGORITHM="HS256",
        JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
    )


@pytest.fixture
def mock_book_collection():
    """Factory fixture that returns a configured mock collection."""
    def _create(book_id: str, title: str, author: str, price: float):
        mock = MagicMock()
        mock.find_one.return_value = {
            "_id": ObjectId(book_id),
            "title": title,
            "author": author,
            "published_date": datetime(2008, 8, 1),
            "genre": "Software",
            "price": price,
        }
        return mock
    return _create
