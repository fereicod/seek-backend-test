from fastapi import APIRouter, HTTPException
from app.core.security import verify_password, create_access_token
from app.repositories.selectors import get_user_repository

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(email: str, password: str) -> dict:
    """Authenticate user and return access token."""

    user_repo = get_user_repository()
    user = user_repo.get_user_by_email(email)

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(
        subject=user.id,
        claims={
            "roles": [role.name for role in user.roles],
            "permissions": [perm for role in user.roles for perm in role.permissions]
        }
    )
    return {"access_token": access_token}