from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_token(token: str = Depends(oauth2_scheme)) -> dict:
    """Decode and validate the JWT token from the Authorization header."""
    try:
        return decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
def require_permission(permission: str) -> callable:
    """Dependency to check if the current token has the required permission."""
    def permission_checker(token: dict = Depends(get_current_token)):
        permissions = token.get("permissions", [])
        if permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return token
    return permission_checker