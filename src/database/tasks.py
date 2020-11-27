from typing import Dict, List
from datetime import datetime
from src.database.base import client
from src.database.users import (
    user_db,
    set_roles_classes, unset_roles_classes,
    set_roles_tasks, unset_roles_tasks,
    set_roles_image_data, unset_roles_image_data
)
from src.database.users import collection as users_collection
from src.models.users import User, UserDB
from src.models.tasks import DBSchema, TaskSchema

system_db_names = ['admin', 'config', 'data_users', 'local']
system_task_names = ['classes', 'info']


async def get_dbs() -> List[str]:
    """

    :param db_name:
    :return:
    """
    db_names = await client.list_database_names()
    # exclude system names
    db_names = list(filter(lambda x: x not in system_db_names, db_names))
    return db_names


async def get_user_tasks(user: User) -> DBSchema:
    if user.is_superuser:
        db_names = await get_dbs()
        tasks = []
        for db_name in db_names:
            task_names = await client[db_name].list_collection_names()
            task_names = list(filter(lambda x: x not in system_task_names, task_names))
            tasks.append(TaskSchema(db_name=db_name, task_names=task_names))
        return DBSchema(db_names=tasks)
    else:
        tasks = []
        for db_name, db_tasks in user.roles_image_data.items():
            task_names = db_tasks.keys()
            task_names = list(filter(lambda x: x not in system_task_names, task_names))
            tasks.append(TaskSchema(db_name=db_name, task_names=task_names))
        return DBSchema(db_names=tasks)


async def get_db_tasks(db_name: str = None) -> DBSchema:
    if db_name is None:
        db_names = await get_dbs()
    else:
        db_names = [db_name]

    tasks = []
    for db_name in db_names:
        task_names = await client[db_name].list_collection_names()
        task_names = list(filter(lambda x: x not in system_task_names, task_names))
        tasks.append(TaskSchema(db_name=db_name, task_names=task_names))
    return DBSchema(db_names=tasks)


async def add_task(db_name: str, task_name: str, user: User = None) -> bool:
    """

    :param db_name:
    :param task_name:
    :return:
    """
    #TODO: edit user rules after add task
    assert task_name not in system_task_names, "Can't add task with this name"
    assert db_name not in system_db_names, "Can't add db with system name"
    db_names = await get_dbs()
    assert db_name in db_names, "DB not exist"
    data_db = client[db_name]
    task_names = await data_db.list_collection_names()
    assert task_name not in task_names, "Task already exist"
    result = await data_db.create_collection(task_name)
    if result:
        if user:
            print('add roles')
            # can add and delete tasks
            await set_roles_image_data(
                db_name=db_name,
                task_name=task_name,
                permissions=[
                    'can_get',
                    'can_add',
                    'can_edit',
                    'can_edit_protected',
                    'can_delete'
                ],
                user=user
            )
        return True
    else:
        return False


async def delete_task(db_name: str, task_name: str) -> bool:
    """
    :param db_name:
    :param task_name:
    :return:
    """
    assert task_name not in system_task_names, "Can't delete task with this name"
    assert db_name not in system_db_names, "Can't add db with system name"
    db_names = await get_dbs()
    assert db_name in db_names, "DB not exist"
    data_db = client[db_name]
    task_names = await data_db.list_collection_names()
    assert task_name in task_names, "task doesn't exist"
    async for user in users_collection.find():
        user = UserDB(**user)
        await unset_roles_image_data(
            db_name=db_name,
            task_name=task_name,
            permissions=[
                'can_get',
                'can_add',
                'can_edit',
                'can_edit_protected',
                'can_delete'
            ],
            user=user
        )
    result = await data_db.drop_collection(task_name)
    if result:
        return True
    else:
        return False


async def add_db(db_name: str, user: User) -> bool:
    """
    :param db_name:
    :return:
    """
    assert db_name not in system_db_names, "Can't add db with system name"
    db_names = await get_dbs()
    assert db_name not in db_names, "DB already exist"
    new_db = client[db_name]
    info_collection = new_db['info']
    info = {
        "created_by": user.id,
        "enterdate": datetime.now(),
    }
    result = await info_collection.insert_one(info)
    if result:
        await set_roles_classes(db_name=db_name, permissions=['can_get', 'can_set'], user=user)
        await set_roles_tasks(db_name=db_name, permissions=['can_add', 'can_delete'], user=user)
        return True
    else:
        return False


async def delete_db(db_name: str) -> bool:
    """
    :param db_name:
    :return:
    """
    assert db_name not in system_db_names, "Can't delete system db"
    db_names = await get_dbs()
    assert db_name in db_names, "DB doesn't exist"
    async for user in users_collection.find():
        user = UserDB(**user)
        await unset_roles_classes(db_name=db_name, permissions=['can_get', 'can_set'], user=user)
        await unset_roles_tasks(db_name=db_name, permissions=['can_add', 'can_delete'], user=user)

        await unset_roles_image_data(
            db_name=db_name,
            task_name=None,
            permissions=[
                'can_get',
                'can_add',
                'can_edit',
                'can_edit_protected',
                'can_delete'
            ],
            user=user
        )
    result = await client.drop_database(db_name)
    return True