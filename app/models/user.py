from pydantic import BaseModel, EmailStr
from typing import Optional

class Role(BaseModel):
    """Role model representing user roles."""
    
    id: Optional[str] = None
    name: str
    permissions: list[str]

class User(BaseModel):
    """User model representing application users."""
    
    id: str
    email: EmailStr
    password_hash: str
    is_active: bool
    roles: list[Role] = []
