import os
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.password import get_password_hash
from src.database.base import client
from src.models.users import UserDB, UserCreate

db = client["data_users"]
collection = db["users"]

user_db = MongoDBUserDatabase(UserDB, collection)


async def create_first_admin() -> bool:

    try:
        count = await collection.count_documents({"is_superuser": True})
        if count == 0:
            user = UserCreate(
                    email=os.getenv('API_ADMIN_EMAIL', 'admin@admin.com'),
                    password=os.getenv('API_ADMIN_PASSWORD', 'adminpassword')
                )
            hashed_password = get_password_hash(user.password)
            db_user = UserDB(
                **user.create_update_dict(), hashed_password=hashed_password
            )
            created_user = await user_db.create(db_user)
            if created_user:
                created_user.is_superuser = True
                updated_user = await user_db.update(created_user)
        return True
    except Exception as e:
        print('exception', e)
        return False
