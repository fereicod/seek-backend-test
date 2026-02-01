from pydantic import BaseModel
from datetime import datetime


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
