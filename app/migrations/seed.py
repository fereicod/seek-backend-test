from datetime import datetime
from app.db.mongo import users_collection, books_collection
from app.core.security import hash_password


# NOTE: Alternative approach using upsert (does not preserve field order):
#
# books_collection.update_one(
#     {"title": "Clean Architecture"},
#     {
#         "$setOnInsert": {
#             "title": "Clean Architecture",
#             "author": "Robert C. Martin",
#             "published_date": datetime(2017, 9, 20),
#             "genre": "Software Engineering",
#             "price": 34.99,
#         }
#     },
#     upsert=True,
# )
#
# The upsert approach is simpler and functional, but MongoDB may reorder fields
# when using $setOnInsert. If field order in documents doesn't matter, use upsert.
# We use insert_one with a check to preserve the exact field order defined below.


def upsert_user(email: str, data: dict):
    """Insert user if not exists."""
    if not users_collection.find_one({"email": email}):
        users_collection.insert_one(data)


def upsert_book(title: str, data: dict):
    """Insert book if not exists."""
    if not books_collection.find_one({"title": title}):
        books_collection.insert_one(data)


# Users
upsert_user(
    "admin@test.com",
    {
        "email": "admin@test.com",
        "password_hash": hash_password("adminpass"),
        "is_active": True,
        "roles": [
            {
                "name": "admin",
                "permissions": [
                    "book:read",
                    "book:create",
                    "book:update",
                    "book:delete",
                    "user:read",
                    "user:create",
                    "user:update",
                    "user:delete",
                ],
            }
        ],
    },
)

upsert_user(
    "editor@test.com",
    {
        "email": "editor@test.com",
        "password_hash": hash_password("editorpass"),
        "is_active": True,
        "roles": [
            {
                "name": "editor",
                "permissions": [
                    "book:read",
                    "book:update",
                ],
            }
        ],
    },
)

# Books
upsert_book(
    "Clean Architecture",
    {
        "title": "Clean Architecture",
        "author": "Robert C. Martin",
        "published_date": datetime(2017, 9, 20),
        "genre": "Software Engineering",
        "price": 34.99,
    },
)

upsert_book(
    "The Pragmatic Programmer",
    {
        "title": "The Pragmatic Programmer",
        "author": "David Thomas, Andrew Hunt",
        "published_date": datetime(2019, 9, 13),
        "genre": "Software Engineering",
        "price": 49.99,
    },
)

upsert_book(
    "Design Patterns",
    {
        "title": "Design Patterns",
        "author": "Gang of Four",
        "published_date": datetime(1994, 10, 31),
        "genre": "Software Engineering",
        "price": 54.99,
    },
)

upsert_book(
    "Refactoring",
    {
        "title": "Refactoring",
        "author": "Martin Fowler",
        "published_date": datetime(2018, 11, 20),
        "genre": "Software Engineering",
        "price": 47.99,
    },
)

upsert_book(
    "Domain-Driven Design",
    {
        "title": "Domain-Driven Design",
        "author": "Eric Evans",
        "published_date": datetime(2003, 8, 30),
        "genre": "Software Engineering",
        "price": 59.99,
    },
)