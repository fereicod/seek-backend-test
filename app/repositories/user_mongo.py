from app.models.user import User
from typing import Any
from bson import ObjectId


class UserMongoRepository:
    """Repository for managing User entities in MongoDB."""

    def __init__(self, collection: Any):
        """Initialize the repository with a MongoDB collection."""
        self.collection = collection

    def _to_user(self, user_data: dict) -> User:
        """Convert MongoDB document to User model."""
        user_data["id"] = str(user_data.pop("_id"))
        return User(**user_data)

    def get_user_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email."""
        user_data = self.collection.find_one({"email": email})
        if user_data:
            return self._to_user(user_data)
        return None

    def get_by_id(self, user_id: str) -> User | None:
        """Retrieve a user by their ID."""
        user_data = self.collection.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return self._to_user(user_data)
        return None
