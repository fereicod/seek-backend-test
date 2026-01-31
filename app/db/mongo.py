from pymongo import MongoClient
from app.core.config import settings

# MongoDB Client Setup
client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

# Collections
users_collection = db["users"]
books_collection = db["books"]
refresh_tokens_collection = db["refresh_tokens"]