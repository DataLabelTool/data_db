from typing import Dict, List
from src.database.base import client
from src.database.classes import set_classes
from src.database.users import user_db
from src.models.users import User
from src.models.tasks import DBSchema, TaskSchema


async def get_dbs() -> List[str]:
    """

    :param db_name:
    :return:
    """
    db_names = await client.database_names()
    db_system_names = ['admin', 'config', 'data_users', 'local']
    # exclude system names
    db_names = list(filter(lambda x: x not in db_system_names, db_names))
    return db_names


async def get_tasks(user: User= None) -> DBSchema:
    """

    :param db_name:
    :return:
    """
    if user is None:
        db_names = get_dbs()
        tasks = []
        for db_name in db_names:
            task_names = await client[db_name].list_collection_names()
            task_system_names = ['classes']
            task_names = list(filter(lambda x: x not in task_system_names, task_names))
            tasks.append(TaskSchema(db_name=db_name, task_names=task_names))
        return DBSchema(db_names=tasks)
    else:
        tasks = []
        for db_name, db_tasks in user.roles_image_data.items():
            task_names = db_tasks.keys()
            task_system_names = ['classes']
            task_names = list(filter(lambda x: x not in task_system_names, task_names))
            tasks.append(TaskSchema(db_name=db_name, task_names=task_names))
        return DBSchema(db_names=tasks)


async def add_task(db_name: str, task_name: str) -> bool:
    """

    :param db_name:
    :param task_name:
    :return:
    """
    #TODO: edit user rules after add task
    assert task_name not in ['classes'], "Can't add task with this name"
    assert db_name not in ['admin', 'config', 'data_users', 'local'], "Can't add db with system name"
    db_names = await client.database_names()
    assert db_name not in db_names, "DB already exist"
    data_db = client[db_name]
    result = await data_db.insert_one([])  #TODO: we should check it
    if result:
        return True
    else:
        return False


async def delete_task(db_name: str, task_name: str) -> bool:
    """
    :param db_name:
    :param task_name:
    :return:
    """
    #TODO: we should clean user roles before delete task
    assert task_name not in ['classes'], "Can't delete task with this name"
    assert db_name not in ['admin', 'config', 'data_users', 'local'], "Can't add db with system name"
    db_names = await client.database_names()
    assert db_name in db_names, "DB not exist"
    data_db = client[db_name]
    task_names = await data_db.list_collection_names()
    assert task_name not in task_names, "task doesn't exist"
    result = await data_db[task_name].drop()
    return True


async def add_db(db_name: str) -> bool:
    """
    :param db_name:
    :return:
    """
    assert db_name not in ['admin', 'config', 'data_users', 'local'], "Can't add db with system name"
    db_names = await client.database_names()
    assert db_name not in db_names, "DB already exist"
    result = await set_classes(classes_data=[], db_name=db_name)
    return True


async def delete_db(db_name: str) -> bool:
    """
    :param db_name:
    :return:
    """
    #TODO: we should clean user roles before delete db
    assert db_name not in ['admin', 'config', 'data_users', 'local'], "Can't delete system db"
    db_names = await client.database_names()
    assert db_name in db_names, "DB doesn't exist"
    result = await client.drop_database(db_name)
    return True