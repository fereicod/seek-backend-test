from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class SortField(str, Enum):
    """Available fields for sorting."""
    PUBLISHED_DATE = "published_date"
    AUTHOR = "author"
    PRICE = "price"
    TITLE = "title"


class SortOrder(str, Enum):
    """Sort order direction."""
    ASC = "asc"
    DESC = "desc"


class BookRequest(BaseModel):
    """Schema for creating a book (all fields required)."""
    title: str
    author: str
    published_date: datetime
    genre: str
    price: float


class BookPatchRequest(BaseModel):
    """Schema for partial update (all fields optional)."""
    title: str | None = None
    author: str | None = None
    published_date: datetime | None = None
    genre: str | None = None
    price: float | None = None


class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    published_date: datetime
    genre: str
    price: float


class SuccessResponse(BaseModel):
    success: bool


class BookMutationResponse(SuccessResponse):
    book: BookResponse | None = None


class CursorPageResponse(BaseModel):
    """Response schema for cursor-based pagination (no total count available)."""
    items: list[BookResponse]
    next_cursor: str | None = None
    has_more: bool = False


class AveragePriceByYear(BaseModel):
    """Average price for a specific year."""
    year: int
    average_price: float
    book_count: int


class AveragePriceByYearResponse(BaseModel):
    """Response schema for average price by year aggregation."""
    data: list[AveragePriceByYear]
