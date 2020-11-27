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


def remove_from_list(arr, val):
    arr = list(set(arr))
    try:
        arr.remove(val)
    except ValueError as e:
        pass
    return arr


def add_to_list(arr, val):
    arr.append(val)
    return list(set(arr))

# dbs
async def set_roles_db(permissions: Union[str, List[str]], user: UserDB):
    if isinstance(permissions, str):
        permissions = [permissions]

    for permission in permissions:
        assert permission in ['can_add', 'can_delete'], "Unknown permission"
        user.roles_db = add_to_list(user.roles_db, permission)
    updated_user = await user_db.update(user)
    return updated_user


async def unset_roles_db(permissions: Union[str, List[str]], user: UserDB):
    if isinstance(permissions, str):
        permissions = [permissions]

    for permission in permissions:
        assert permission in ['can_add', 'can_delete'], "Unknown permission"
        user.roles_db = remove_from_list(user.roles_db, permission)
    updated_user = await user_db.update(user)
    return updated_user


# tasks
async def set_roles_tasks(db_name: str, permissions: Union[str, List[str]], user: UserDB):
    if isinstance(permissions, str):
        permissions = [permissions]

    for permission in permissions:
        assert permission in ['can_add', 'can_delete'], "Unknown permission"
        user.roles_tasks[db_name] = add_to_list(
            user.roles_tasks.get(db_name, []),
            permission
        )
    updated_user = await user_db.update(user)
    return updated_user


async def unset_roles_tasks(db_name: str, permissions: Union[str, List[str]], user: UserDB):
    if isinstance(permissions, str):
        permissions = [permissions]

    for permission in permissions:
        assert permission in ['can_add', 'can_delete'], "Unknown permission"
        roles_tasks = remove_from_list(user.roles_tasks.get(db_name, []), permission)
        if len(roles_tasks) > 0:
            user.roles_tasks[db_name] = roles_tasks
        else:
            user.roles_tasks.pop(db_name, None)
    updated_user = await user_db.update(user)
    return updated_user

# classes
async def set_roles_classes(db_name: str, permissions: Union[str, List[str]], user: UserDB):
    if isinstance(permissions, str):
        permissions = [permissions]
    for permission in permissions:
        assert permission in ['can_get', 'can_set'], "Unknown permission"
        user.roles_classes[db_name] = add_to_list(
            user.roles_classes.get(db_name, []),
            permission
        )
    updated_user = await user_db.update(user)
    return updated_user


async def unset_roles_classes(db_name: str, permissions: Union[str, List[str]], user: UserDB):
    print(user)
    if isinstance(permissions, str):
        permissions = [permissions]
    for permission in permissions:
        assert permission in ['can_get', 'can_set'], "Unknown permission"
        roles_classes = remove_from_list(
            user.roles_classes.get(db_name, []),
            permission
        )
        if len(roles_classes) > 0:
            user.roles_classes[db_name] = roles_classes
        else:
            user.roles_classes.pop(db_name, None)
    updated_user = await user_db.update(user)
    return updated_user


# image_data
async def set_roles_image_data(db_name: str, task_name: str, permissions: Union[str, List[str]], user: UserDB):
    if isinstance(permissions, str):
        permissions = [permissions]
    for permission in permissions:
        assert permission in ['can_get', 'can_edit', 'can_edit_protected', 'can_add', 'can_delete'], "Unknown permission"
        roles_image_data = user.roles_image_data.get(db_name, {})
        roles_image_data_task = add_to_list(roles_image_data.get(task_name, []), permission)
        roles_image_data[task_name] = roles_image_data_task
        user.roles_image_data[db_name] = roles_image_data
    updated_user = await user_db.update(user)
    return updated_user


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
                    task_roles = remove_from_list(task_roles, permission)
                    if len(task_roles) > 0:
                        user.roles_image_data[db_name][task_name] = task_roles
                    else:
                        user.roles_image_data[db_name].pop(task_name, None)
    roles_image_data = user.roles_image_data.get(db_name, {})
    if len(roles_image_data) == 0:
        user.roles_image_data.pop(db_name, None)

    updated_user = await user_db.update(user)
    return updated_user
