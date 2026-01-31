from app.db.mongo import books_collection, users_collection
from app.repositories.book_mongo import BookMongoRepository
from app.repositories.user_mongo import UserMongoRepository

def get_book_repository() -> BookMongoRepository:
    return BookMongoRepository(books_collection)

def get_user_repository() -> UserMongoRepository:
    return UserMongoRepository(users_collection)