from pydantic import BaseModel, EmailStr

class Role(BaseModel):
    """Role model representing user roles."""
    
    id: str
    name: str
    permissions: list[str]

class User(BaseModel):
    """User model representing application users."""
    
    id: str
    email: EmailStr
    password_hash: str
    is_active: bool = True
    roles: list[Role] = []
