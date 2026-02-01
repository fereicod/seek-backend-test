from fastapi import APIRouter, Depends
from app.core.dependencies import require_permission
from app.repositories.selectors import get_book_repository
from app.schemas.book import BookRequest, BookPatchRequest, BookResponse, BookMutationResponse, SuccessResponse

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=list[BookResponse], dependencies=[Depends(require_permission("book:read"))])
def list_books() -> list[BookResponse]:
    """Retrieve a list of books."""

    book_repo = get_book_repository()
    books = book_repo.list_books()

    return books

@router.get("/{book_id}", response_model=BookResponse, dependencies=[Depends(require_permission("book:read"))])
def get_book(book_id: str) -> BookResponse:
    """Retrieve a book by its ID."""

    book_repo = get_book_repository()
    book = book_repo.get_book_by_id(book_id=book_id)

    return book

@router.post("/", response_model=BookMutationResponse, dependencies=[Depends(require_permission("book:create"))])
def create_book(book: BookRequest) -> BookMutationResponse:
    """Create a new book."""

    book_repo = get_book_repository()
    success, new_book = book_repo.create_book(book=book)

    book_response = BookResponse(**new_book.model_dump()) if new_book else None
    return BookMutationResponse(success=success, book=book_response)

@router.put("/{book_id}", response_model=BookMutationResponse, dependencies=[Depends(require_permission("book:update"))])
def update_book(book_id: str, book: BookRequest) -> BookMutationResponse:
    """Full update of an existing book (all fields required)."""

    book_repo = get_book_repository()
    success, updated_book = book_repo.update_book(book_id=book_id, updated_data=book.model_dump())

    book_response = BookResponse(**updated_book.model_dump()) if updated_book else None
    return BookMutationResponse(success=success, book=book_response)


@router.patch("/{book_id}", response_model=BookMutationResponse, dependencies=[Depends(require_permission("book:update"))])
def patch_book(book_id: str, book: BookPatchRequest) -> BookMutationResponse:
    """Partial update of an existing book (only provided fields)."""

    book_repo = get_book_repository()
    success, updated_book = book_repo.patch_book(book_id=book_id, patch_data=book.model_dump())

    book_response = BookResponse(**updated_book.model_dump()) if updated_book else None
    return BookMutationResponse(success=success, book=book_response)

@router.delete("/{book_id}", response_model=SuccessResponse, dependencies=[Depends(require_permission("book:delete"))])
def delete_book(book_id: str) -> SuccessResponse:
    """Delete a book by its ID."""

    book_repo = get_book_repository()
    success = book_repo.delete_book(book_id=book_id)

    return SuccessResponse(success=success)