from pydantic import BaseModel
from datetime import datetime


class BookRequest(BaseModel):
    title: str
    author: str
    published_date: datetime
    genre: str
    price: float

class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    published_date: datetime
    genre: str
    price: float


class SuccessResponse(BaseModel):
    success: bool


class BookUpdateResponse(SuccessResponse):
    book: BookResponse | None = None
