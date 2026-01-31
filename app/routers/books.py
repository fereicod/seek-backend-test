from fastapi import APIRouter
from app.repositories.selectors import get_book_repository

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=list[dict])
def list_books() -> list[dict]:
    """Retrieve a list of books."""
    
    book_repo = get_book_repository()
    books = book_repo.list_books()
    
    return books