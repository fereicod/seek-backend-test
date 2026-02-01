from pydantic import BaseModel
from datetime import datetime


class Book(BaseModel):
    """Book model representing a book in the library."""

    id: str
    title: str
    author: str
    published_date: datetime
    genre: str
    price: float
