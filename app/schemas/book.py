from pydantic import BaseModel
from datetime import datetime


class BookResponse(BaseModel):
    id: str
    title: str
    author: str
    published_date: datetime
    genre: str
    price: float
