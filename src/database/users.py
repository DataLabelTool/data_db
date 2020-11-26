import os
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.password import get_password_hash
from src.database.base import client
from src.models.users import UserDB, UserCreate

db = client["data_users"]
collection = db["users"]

user_db = MongoDBUserDatabase(UserDB, collection)


async def count_superusers() -> bool:
    count = await collection.count_documents({"is_superuser": True})
    return count

