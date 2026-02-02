"""Unit tests for BookMongoRepository using mocks."""
from app.repositories.book_mongo import BookMongoRepository


def test_get_book_by_id_with_mock(mock_book_collection):
    """Repository should use collection.find_one and convert _id to string."""
    book_id = "507f1f77bcf86cd799439011"
    mock_collection = mock_book_collection(
        book_id=book_id,
        title="Clean Code",
        author="Robert Martin",
        price=39.99
    )

    repo = BookMongoRepository(mock_collection)
    book = repo.get_book_by_id(book_id)
    
    mock_collection.find_one.assert_called_once()
    assert book.id == book_id
    assert book.title == "Clean Code"
    assert book.price == 39.99