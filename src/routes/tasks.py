from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder

from src.database.tasks import (
    get_tasks,
    add_task,
    delete_task,
    add_db,
    delete_db
)
from src.models.tasks import (
    ErrorResponseModel,
    ResponseModel,
    TaskSchema,
    DBSchema,
)
from src.models.users import User
from src.routes.users import fastapi_users

tasks_router = APIRouter()


@tasks_router.get("/", response_description="Tasks dict retrieved")
async def get_tasks_route(
        user: User = Depends(fastapi_users.get_current_active_user)
):
    """return db_names and tasks available for user"""
    tasks = await get_tasks(user)
    if tasks:
        return ResponseModel(tasks, "tasks data retrieved successfully")
    else:
        return ErrorResponseModel(
                "An error occurred",
                503,
                "empty task dict"
            )


@tasks_router.post("/", response_description="Task added into the database")
async def add_task_route(
        db_name: str,
        task_name: str,
        user: User = Depends(fastapi_users.get_current_active_user)
):
    """"""
    try:
        if user.can_add_tasks(db_name=db_name):
            result = await add_task(db_name=db_name, task_name=task_name)
            if result:
                return ResponseModel(result, "task add successfully")
            else:
                return ErrorResponseModel(
                    "An error occurred",
                    503,
                    "empty task dict"
                )
        else:
            return ErrorResponseModel(
                "An error occurred",
                503,
                "User can't add tasks"
            )
    except Exception as e:
        return ErrorResponseModel(
            "An error occurred",
            503,
            e.__str__()
        )



@tasks_router.delete("/", response_description="Task deleted from the database")
async def delete_task_route(
        db_name: str,
        task_name: str,
        user: User = Depends(fastapi_users.get_current_active_user)
):
    try:
        if user.can_delete_tasks(db_name=db_name):
            result = await delete_task(db_name=db_name, task_name=task_name)
            if result:
                return ResponseModel(result, "tasks deleted successfully")
            else:
                return ErrorResponseModel(
                    "An error occurred",
                    503,
                    "empty task dict"
                )
        else:
            return ErrorResponseModel(
                "An error occurred",
                503,
                "User can't delete tasks"
            )
    except Exception as e:
        return ErrorResponseModel(
            "An error occurred",
            503,
            e.__str__()
        )



dbs_router = APIRouter()


@dbs_router.post("/", response_description="Db added into the database")
async def add_db_route(
        db_name: str,
        user: User = Depends(fastapi_users.get_current_active_user)
):
    try:
        if user.can_add_dbs():
            result = await add_db(db_name=db_name, user=user)
            if result:
                return ResponseModel(result, "db add successfully")
            else:
                return ErrorResponseModel(
                    "An error occurred",
                    503,
                    "empty db result"
                )
        else:
            return ErrorResponseModel(
                "An error occurred",
                503,
                "User can't add dbs"
            )
    except Exception as e:
        return ErrorResponseModel(
            "An error occurred",
            503,
            e.__str__()
        )


@dbs_router.delete("/", response_description="Db deleted from the database")
async def delete_db_route(
        db_name: str,
        user: User = Depends(fastapi_users.get_current_active_user)
):
    try:
        if user.can_delete_dbs():
            result = await delete_db(db_name=db_name)
            if result:
                return ResponseModel(result, "db deleted successfully")
            else:
                return ErrorResponseModel(
                    "An error occurred",
                    503,
                    "empty db result"
                )
        else:
            return ErrorResponseModel(
                "An error occurred",
                503,
                "User can't delete dbs"
            )
    except Exception as e:
        return ErrorResponseModel(
            "An error occurred",
            503,
            e.__str__()
        )