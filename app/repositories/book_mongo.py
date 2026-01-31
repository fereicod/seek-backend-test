from app.models.book import Book
from typing import Any

class BookMongoRepository:
    """Repository for managing Book entities in MongoDB."""

    def __init__(self, mongo_client: Any):
        """Initialize the repository with a MongoDB client."""
        self.collection = mongo_client.db.books

    def add_book(self, book: Book) -> str:
        """Add a new book to the collection."""
        book_dict = book.dict()
        result = self.collection.insert_one(book_dict)
        return str(result.inserted_id)

    def get_book_by_id(self, book_id: str) -> Book | None:
        """Retrieve a book by its ID."""
        book_data = self.collection.find_one({"_id": book_id})
        if book_data:
            return Book(**book_data)
        return None

    def update_book(self, book_id: str, updated_data: dict) -> bool:
        """Update an existing book's data."""
        result = self.collection.update_one({"_id": book_id}, {"$set": updated_data})
        return result.modified_count > 0

    def delete_book(self, book_id: str) -> bool:
        """Delete a book by its ID."""
        result = self.collection.delete_one({"_id": book_id})
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