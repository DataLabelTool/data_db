import os
from typing import Union, List
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


# dbs
async def set_roles_db(permissions: Union[str, List[str]], user: UserDB):
    if isinstance(permissions, str):
        permissions = [permissions]

    for permission in permissions:
        assert permission in ['can_add', 'can_delete'], "Unknown permission"
        user.roles_db.add(permission)
    updated_user = await user_db.update(user)


async def unset_roles_db(permissions: Union[str, List[str]], user: UserDB):
    if isinstance(permissions, str):
        permissions = [permissions]

    for permission in permissions:
        assert permission in ['can_add', 'can_delete'], "Unknown permission"
        user.roles_db.discard(permission)
    updated_user = await user_db.update(user)


# tasks
async def set_roles_tasks(db_name: str, permissions: Union[str, List[str]], user: UserDB):
    if isinstance(permissions, str):
        permissions = [permissions]

    for permission in permissions:
        assert permission in ['can_add', 'can_delete'], "Unknown permission"
        roles_tasks = user.roles_tasks.get(db_name, set()).add(permission)
        user.roles_tasks[db_name] = roles_tasks
    updated_user = await user_db.update(user)


async def unset_roles_tasks(db_name: str, permissions: Union[str, List[str]], user: UserDB):
    if isinstance(permissions, str):
        permissions = [permissions]

    for permission in permissions:
        assert permission in ['can_add', 'can_delete'], "Unknown permission"
        roles_tasks = user.roles_tasks.get(db_name, set()).discard(permission)
        if len(roles_tasks) > 0:
            user.roles_tasks[db_name] = roles_tasks
        else:
            user.roles_tasks.pop(db_name, None)
    updated_user = await user_db.update(user)

# classes
async def set_roles_classes(db_name: str, permissions: Union[str, List[str]], user: UserDB):
    if isinstance(permissions, str):
        permissions = [permissions]
    for permission in permissions:
        assert permission in ['can_get', 'can_set'], "Unknown permission"
        roles_classes = user.roles_classes.get(db_name, set()).add(permission)
        user.roles_classes[db_name] = roles_classes
    updated_user = await user_db.update(user)


async def unset_roles_classes(db_name: str, permissions: Union[str, List[str]], user: UserDB):
    if isinstance(permissions, str):
        permissions = [permissions]
    for permission in permissions:
        assert permission in ['can_get', 'can_set'], "Unknown permission"
        roles_classes = user.roles_classes.get(db_name, set()).discard(permission)
        if len(roles_classes) > 0:
            user.roles_classes[db_name] = roles_classes
        else:
            user.roles_classes.pop(db_name, None)
    updated_user = await user_db.update(user)


# image_data
async def set_roles_image_data(db_name: str, task_name: str, permissions: Union[str, List[str]], user: UserDB):
    if isinstance(permissions, str):
        permissions = [permissions]
    for permission in permissions:
        assert permission in ['can_get', 'can_edit', 'can_edit_protected', 'can_add', 'can_delete'], "Unknown permission"
        roles_image_data = user.roles_image_data.get(db_name, {})
        roles_image_data[task_name].add(permission)
        user.roles_image_data[db_name] = roles_image_data
    updated_user = await user_db.update(user)


async def unset_roles_image_data(db_name: str, task_name: Union[str, None], permissions: Union[str, List[str]], user: UserDB):
    if isinstance(permissions, str):
        permissions = [permissions]
    for permission in permissions:
        assert permission in ['can_get', 'can_edit', 'can_edit_protected', 'can_add', 'can_delete'], "Unknown permission"
        roles_image_data = user.roles_image_data.get(db_name, {})
        if len(roles_image_data) > 0:
            if task_name is not None:
                task_names = [task_name]
            else:
                task_names = roles_image_data.keys()
            for task_name in task_names:
                task_roles = roles_image_data.get(task_name, None)
                if task_roles is not None:
                    task_roles.discard(permission)
                    if len(task_roles) > 0:
                        user.roles_image_data[db_name][task_name] = task_roles
                    else:
                        user.roles_image_data[db_name].pop(task_name, None)
    roles_image_data = user.roles_image_data.get(db_name, {})
    if len(roles_image_data) == 0:
        user.roles_image_data.pop(db_name, None)

    updated_user = await user_db.update(user)
