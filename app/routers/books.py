from fastapi import APIRouter, Depends
from app.core.dependencies import require_permission
from app.repositories.selectors import get_book_repository

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=list[dict], dependencies=[Depends(require_permission("book:read"))])
def list_books() -> list[dict]:
    """Retrieve a list of books."""
    
    book_repo = get_book_repository()
    books = book_repo.list_books()
    
    return books