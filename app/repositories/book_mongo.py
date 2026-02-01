from app.models.book import Book
from app.schemas.book import BookRequest
from typing import Any
from uuid import uuid4


class BookMongoRepository:
    """Repository for managing Book entities in MongoDB."""

    def __init__(self, collection: Any):
        """Initialize the repository with a MongoDB client."""
        self.collection = collection

    def get_book_by_id(self, book_id: str) -> Book | None:
        """Retrieve a book by its ID."""
        book_data = self.collection.find_one({"id": book_id})
        if book_data:
            return Book(**book_data)
        return None

    def create_book(self, book: BookRequest) -> Book:
        """Create a new book and return the complete book with ID."""
        book_data = book.model_dump()
        book_data["id"] = str(uuid4())
        self.collection.insert_one(book_data)
        return Book(**book_data)

    def update_book(self, book_id: str, updated_data: dict) -> tuple[bool, Book | None]:
        """Update an existing book's data and return the updated book."""
        result = self.collection.update_one({"id": book_id}, {"$set": updated_data})
        if result.matched_count > 0:
            return True, self.get_book_by_id(book_id)
        return False, None

    def delete_book(self, book_id: str) -> bool:
        """Delete a book by its ID."""
        result = self.collection.delete_one({"id": book_id})
        return result.deleted_count > 0

    # ToDo: Implement additional methods as needed, e.g., list all books, skip, limit, aggregate functions, etc.
    def list_books(self) -> list[Book]:
        """List all books in the collection."""
        books = self.collection.find()
        return [Book(**book) for book in books]
    
    def average_price_by_year(self, year: int) -> float:
        """Calculate the average price of books published in a given year."""
        pipeline = [
            {"$match": {"published_date": {"$gte": f"{year}-01-01", "$lt": f"{year+1}-01-01"}}},
            {"$group": {"_id": None, "average_price": {"$avg": "$price"}}}
        ]
        result = list(self.collection.aggregate(pipeline))
        return float(result[0]['average_price']) if result else 0.0