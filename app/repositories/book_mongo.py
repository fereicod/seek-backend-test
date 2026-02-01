import re
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

    def _build_filter_query(
        self,
        author: str | None = None,
        title: str | None = None,
        genre: str | None = None,
    ) -> dict:
        """
        Build MongoDB filter query from optional parameters.
        Uses regex for partial, case-insensitive matching.
        """
        query = {}
        if author:
            query["author"] = {"$regex": re.escape(author), "$options": "i"}
        if title:
            query["title"] = {"$regex": re.escape(title), "$options": "i"}
        if genre:
            query["genre"] = {"$regex": re.escape(genre), "$options": "i"}
        return query

    def _build_sort(
        self,
        sort_by: str | None = None,
        sort_order: str = "asc",
    ) -> list[tuple[str, int]]:
        """
        Build MongoDB sort specification.
        Returns list of tuples: [(field, direction), ...]
        """
        if not sort_by:
            return [("_id", 1)]  # Default sort by _id ascending

        direction = 1 if sort_order == "asc" else -1
        # Always add _id as secondary sort for consistency
        return [(sort_by, direction), ("_id", direction)]

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

    def count_books(
        self,
        author: str | None = None,
        title: str | None = None,
        genre: str | None = None,
    ) -> int:
        """Count total number of books matching filters."""
        query = self._build_filter_query(author=author, title=title, genre=genre)
        return self.collection.count_documents(query)

    def list_books_paginated(
        self,
        skip: int = 0,
        limit: int = 10,
        sort_by: str | None = None,
        sort_order: str = "asc",
        author: str | None = None,
        title: str | None = None,
        genre: str | None = None,
    ) -> list[Book]:
        """
        List books with skip/limit pagination, sorting and filtering.
        Used by Page and LimitOffset pagination.
        """
        query = self._build_filter_query(author=author, title=title, genre=genre)
        sort = self._build_sort(sort_by=sort_by, sort_order=sort_order)

        books = self.collection.find(query).sort(sort).skip(skip).limit(limit)
        return [self._to_book(book) for book in books]
    
    def get_average_price_by_year(self, year: int | None = None) -> list[dict]:
        """
        Calculate the average price of books grouped by publication year.
        Uses MongoDB aggregation pipeline with $year operator.
        
        Args:
            year: Optional filter for a specific year. If None, returns all years.
        
        Returns:
            List of dicts with year, average_price, and book_count.
        """
        pipeline = []
        
        # Optional filter by specific year
        if year is not None:
            pipeline.append({
                "$match": {
                    "$expr": {
                        "$eq": [{"$year": "$published_date"}, year]
                    }
                }
            })
        
        # Group by year extracted from published_date
        pipeline.append({
            "$group": {
                "_id": {"$year": "$published_date"},
                "average_price": {"$avg": "$price"},
                "book_count": {"$sum": 1}
            }
        })
        
        # Sort by year descending (most recent first)
        pipeline.append({"$sort": {"_id": -1}})
        
        # Project to rename _id to year
        pipeline.append({
            "$project": {
                "_id": 0,
                "year": "$_id",
                "average_price": {"$round": ["$average_price", 2]},
                "book_count": 1
            }
        })
        
        return list(self.collection.aggregate(pipeline))