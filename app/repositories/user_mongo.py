from app.models.user import User
from typing import Any

class UserMongoRepository:
    """Repository for managing User entities in MongoDB."""

    def __init__(self, collection: Any):
        """Initialize the repository with a MongoDB collection."""
        self.collection = collection

    def get_user_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email."""
        user_data = self.collection.find_one({"email": email})
        if user_data:
            return User(**user_data)
        return None
    
    def get_by_id(self, user_id: str) -> User | None:
        """Retrieve a user by their ID."""
        user_data = self.collection.find_one({"_id": user_id})
        if user_data:
            return User(**user_data)
        return None
