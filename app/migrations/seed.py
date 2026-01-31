from uuid import uuid4
from datetime import datetime
from app.db.mongo import users_collection, books_collection
from app.core.security import hash_password

users_collection.update_one(
    {"email": "admin@test.com"},
    {
        "$setOnInsert": {
            "id": str(uuid4()),
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
                        "user:delete"
                    ]
                }
            ]
        }
    },
    upsert=True
)

users_collection.update_one(
    {"email": "editor@test.com"},
    {
        "$setOnInsert": {
            "id": str(uuid4()),
            "email": "editor@test.com",
            "password_hash": hash_password("editorpass"),
            "is_active": True,
            "roles": [
                {
                    "name": "editor",
                    "permissions": [
                        "book:read",
                        "book:update"
                    ]
                }
            ]
        }
    },
    upsert=True
)

books_collection.update_one(
    {"title": "Clean Architecture"},
    {
        "$setOnInsert": {
            "id": str(uuid4()),
            "title": "Clean Architecture",
            "author": "Robert C. Martin",
            "published_date": datetime(2017, 9, 20),
            "genre": "Software Engineering",
            "price": 34.99
        }
    },
    upsert=True
)

books_collection.update_one(
    {"title": "The Pragmatic Programmer"},
    {
        "$setOnInsert": {
            "id": str(uuid4()),
            "title": "The Pragmatic Programmer",
            "author": "David Thomas, Andrew Hunt",
            "published_date": datetime(2019, 9, 13),
            "genre": "Software Engineering",
            "price": 49.99
        }
    },
    upsert=True
)

books_collection.update_one(
    {"title": "Design Patterns"},
    {
        "$setOnInsert": {
            "id": str(uuid4()),
            "title": "Design Patterns",
            "author": "Gang of Four",
            "published_date": datetime(1994, 10, 31),
            "genre": "Software Engineering",
            "price": 54.99
        }
    },
    upsert=True
)

books_collection.update_one(
    {"title": "Refactoring"},
    {
        "$setOnInsert": {
            "id": str(uuid4()),
            "title": "Refactoring",
            "author": "Martin Fowler",
            "published_date": datetime(2018, 11, 20),
            "genre": "Software Engineering",
            "price": 47.99
        }
    },
    upsert=True
)

books_collection.update_one(
    {"title": "Domain-Driven Design"},
    {
        "$setOnInsert": {
            "id": str(uuid4()),
            "title": "Domain-Driven Design",
            "author": "Eric Evans",
            "published_date": datetime(2003, 8, 30),
            "genre": "Software Engineering",
            "price": 59.99
        }
    },
    upsert=True
)