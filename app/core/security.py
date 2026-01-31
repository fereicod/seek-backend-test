from datetime import datetime, timedelta
from jwt import encode
import bcrypt
from app.core.config import settings


def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password."""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def create_access_token(subject: str, claims: dict, expires_delta: timedelta = None) -> str:
    """Create a JWT access token."""
    payload = {
        "sub": subject,
        **claims,
        "exp": datetime.utcnow() + (expires_delta or timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    }
    return encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
