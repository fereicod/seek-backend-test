from fastapi import APIRouter, Depends
from app.core.dependencies import require_permission
from app.repositories.selectors import get_book_repository
from app.schemas.book import BookResponse

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=list[BookResponse], dependencies=[Depends(require_permission("book:read"))])
def list_books() -> list[BookResponse]:
    """Retrieve a list of books."""

    book_repo = get_book_repository()
    books = book_repo.list_books()

    return books