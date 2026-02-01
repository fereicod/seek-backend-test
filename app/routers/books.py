from fastapi import APIRouter, Depends, Query
from fastapi_pagination import Params
from fastapi_pagination.links import Page
from app.core.dependencies import require_permission
from app.repositories.selectors import get_book_repository
from app.schemas.book import (
    BookRequest,
    BookPatchRequest,
    BookResponse,
    BookMutationResponse,
    SuccessResponse,
    SortField,
    SortOrder,
    AveragePriceByYearResponse,
    AveragePriceByYear,
)

router = APIRouter(prefix="/books", tags=["Books"])

@router.get(
    "/",
    response_model=Page[BookResponse],
    dependencies=[Depends(require_permission("book:read"))],
)
def list_books_page(
    params: Params = Depends(),
    # Sorting
    sort_by: SortField | None = Query(None, description="Field to sort by"),
    sort_order: SortOrder = Query(SortOrder.ASC, description="Sort direction"),
    # Filtering
    author: str | None = Query(None, description="Filter by author (partial match)"),
    title: str | None = Query(None, description="Filter by title (partial match)"),
    genre: str | None = Query(None, description="Filter by genre (partial match)"),
) -> Page[BookResponse]:
    """
    List books with PAGE pagination, sorting and filtering.

    **Pagination**: ?page=1&size=10\n
    **Sorting**: ?sort_by=price&sort_order=desc\n
    **Filtering**: ?author=Martin&genre=Software\n
    **Mixed**: ?page=2&size=5&sort_by=published_date&sort_order=asc&title=Python
    """
    book_repo = get_book_repository()

    total = book_repo.count_books(author=author, title=title, genre=genre)
    skip = (params.page - 1) * params.size
    books = book_repo.list_books_paginated(
        skip=skip,
        limit=params.size,
        sort_by=sort_by.value if sort_by else None,
        sort_order=sort_order.value,
        author=author,
        title=title,
        genre=genre,
    )

    return Page.create(items=books, params=params, total=total)


@router.get(
    "/stats/average-price-by-year",
    response_model=AveragePriceByYearResponse,
    dependencies=[Depends(require_permission("book:read"))],
)
def get_average_price_by_year(
    year: int | None = Query(None, description="Filter by specific year (optional)"),
) -> AveragePriceByYearResponse:
    """
    Get average book price grouped by publication year.
    
    Uses MongoDB aggregation pipeline to calculate:
    - Average price per year
    - Number of books per year
    
    **All years**: GET /stats/average-price-by-year\n
    **Specific year**: GET /stats/average-price-by-year?year=2023
    """
    book_repo = get_book_repository()
    results = book_repo.get_average_price_by_year(year=year)
    
    data = [AveragePriceByYear(**item) for item in results]
    return AveragePriceByYearResponse(data=data)


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

