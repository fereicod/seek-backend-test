from datetime import datetime, timedelta
from jwt import encode
from passlib.context import CryptContext
from app.core.config import settings

# Define password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: str, claims: dict, expires_delta: timedelta = None) -> str:
    """Create a JWT access token."""
    payload = {
        "sub": subject,
        **claims,
        "exp": datetime.utcnow() + (expires_delta or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    }
    return encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
