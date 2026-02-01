from app.models.book import Book
from app.schemas.book import BookRequest
from typing import Any
from bson import ObjectId


class BookMongoRepository:
    """Repository for managing Book entities in MongoDB."""

    def __init__(self, collection: Any):
        """Initialize the repository with a MongoDB client."""
        self.collection = collection

    def _to_book(self, book_data: dict) -> Book:
        """Convert MongoDB document to Book model."""
        book_data["id"] = str(book_data.pop("_id"))
        return Book(**book_data)

    def get_book_by_id(self, book_id: str) -> Book | None:
        """Retrieve a book by its ID."""
        book_data = self.collection.find_one({"_id": ObjectId(book_id)})
        if book_data:
            return self._to_book(book_data)
        return None

    def create_book(self, book: BookRequest) -> tuple[bool, Book | None]:
        """Create a new book and return success status with the book."""
        try:
            book_data = book.model_dump()
            result = self.collection.insert_one(book_data)
            # Avoid extra query to find book, use the inserted_id directly
            book_data["_id"] = result.inserted_id
            return True, self._to_book(book_data)
        except Exception:
            return False, None

    def update_book(self, book_id: str, updated_data: dict) -> tuple[bool, Book | None]:
        """
        Full update: Replace all fields with the provided data.
        Returns the updated book using the sent data (no extra query).
        """
        result = self.collection.update_one({"_id": ObjectId(book_id)}, {"$set": updated_data})
        if result.matched_count > 0:
            # Reuse sent data instead of querying again
            updated_data["id"] = book_id
            return True, Book(**updated_data)
        return False, None

    def patch_book(self, book_id: str, patch_data: dict) -> tuple[bool, Book | None]:
        """
        Partial update: Only update the provided fields.
        Merges with existing data to return complete book.
        """
        # Remove None values from patch_data
        patch_data = {k: v for k, v in patch_data.items() if v is not None}
        if not patch_data:
            return False, None
        
        result = self.collection.update_one({"_id": ObjectId(book_id)}, {"$set": patch_data})
        if result.matched_count > 0:
            # Need to get full book since we only have partial data
            return True, self.get_book_by_id(book_id)
        return False, None

    def delete_book(self, book_id: str) -> bool:
        """Delete a book by its ID."""
        result = self.collection.delete_one({"_id": ObjectId(book_id)})
        return result.deleted_count > 0

    # ToDo: Implement additional methods as needed, e.g., list all books, skip, limit, aggregate functions, etc.
    def list_books(self) -> list[Book]:
        """List all books in the collection."""
        books = self.collection.find()
        return [self._to_book(book) for book in books]
    
    def average_price_by_year(self, year: int) -> float:
        """Calculate the average price of books published in a given year."""
        pipeline = [
            {"$match": {"published_date": {"$gte": f"{year}-01-01", "$lt": f"{year+1}-01-01"}}},
            {"$group": {"_id": None, "average_price": {"$avg": "$price"}}}
        ]
        result = list(self.collection.aggregate(pipeline))
        return float(result[0]['average_price']) if result else 0.0