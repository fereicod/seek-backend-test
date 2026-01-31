from pydantic import BaseModel
from datetime import date

class Book(BaseModel):
    """Book model representing a book in the library."""
    
    id: str
    title: str
    author: str
    published_date: date
    genre: str
    price: float
