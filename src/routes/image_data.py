from typing import Optional, Union
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder

from src.database.image_data import (
    get_image_data_ids,
    get_image_data,
    update_image_data,
    delete_image_data,
    add_image_data
)
from src.models.image_data import (
    ErrorResponseModel,
    ResponseModel,
    ImageDataSchema,
    UpdateImageDataModel,
)
from src.models.users import User
from src.routes.users import fastapi_users

image_data_router = APIRouter()


@image_data_router.get("/", response_description="Image Data retrieved")
async def get_image_data_route(
        db_name: str,
        task_name: str,
        id: Optional[str] = None,
        user: User = Depends(fastapi_users.get_current_active_user)
):
    try:
        if id is None:
            if user.can_get_image_data(db_name=db_name, task_name=task_name):
                ids = await get_image_data_ids(db_name, task_name)
                if ids:
                    return ResponseModel(ids, "Image Data ids retrieved successfully")
                return ResponseModel([], "Image Data ids are empty")
            else:
                return ErrorResponseModel(
                    "An error occurred",
                    503,
                    "User can't get Image Data."
                )
        else:
            if user.can_get_image_data(db_name=db_name, task_name=task_name):
                image_data = await get_image_data(db_name, task_name, id)
                if image_data:
                    return ResponseModel(image_data, "Image Data retrieved successfully")
                return ResponseModel({}, "Image Data are empty")
            else:
                return ErrorResponseModel(
                    "An error occurred",
                    503,
                    "User can't get Image Data."
                )
    except Exception as e:
        return ErrorResponseModel(
            "An error occurred",
            503,
            e.__str__()
        )


@image_data_router.post("/", response_description="Image Data added into the database")
async def add_image_data_route(
        db_name: str,
        task_name: str,
        id: Optional[str] = None,
        image_data: Union[ImageDataSchema, UpdateImageDataModel] = Body(...),
        user: User = Depends(fastapi_users.get_current_active_user)
):
    try:
        if id is None:
            if user.can_add_image_data(db_name=db_name, task_name=task_name):
                image_data = jsonable_encoder(image_data, exclude_none=True)
                result = await add_image_data(
                    db_name=db_name,
                    task_name=task_name,
                    image_data=image_data
                )
                if result:
                    return ResponseModel(result, "Image Data added successfully.")
                return ErrorResponseModel(
                    "An error occurred",
                    404,
                    "Can't add Image Data"
                )
            else:
                return ErrorResponseModel(
                    "An error occurred",
                    503,
                    "User can't update Image Data"
                )
        else:
            can_edit_protected = user.can_edit_protected_image_data(db_name=db_name, task_name=task_name)
            if user.can_edit_image_data(db_name=db_name, task_name=task_name) or can_edit_protected:
                image_data = jsonable_encoder(image_data, exclude_none=True)
                result = await update_image_data(
                    db_name=db_name,
                    task_name=task_name,
                    id=id,
                    image_data=image_data,
                    check_protected=can_edit_protected
                )
                if result:
                    return ResponseModel(result, "Image Data updated successfully.")
                return ErrorResponseModel(
                    "An error occurred",
                    404,
                    "Can't update Image Data"
                )
            else:
                return ErrorResponseModel(
                    "An error occurred",
                    503,
                    "User can't update Image Data"
                )
    except Exception as e:
        return ErrorResponseModel(
            "An error occurred",
            503,
            e.__str__()
        )


@image_data_router.delete("/", response_description="Image Data deleted from the database")
async def delete_image_data_route(
        db_name: str,
        task_name: str,
        id: str,
        user: User = Depends(fastapi_users.get_current_active_user)
):
    try:
        if user.can_delete_image_data(db_name=db_name, task_name=task_name):
            result = await delete_image_data(db_name=db_name, task_name=task_name, id=id)
            if result:
                return ResponseModel(
                    "Image with ID: {} removed".format(id),
                    "Image Data deleted successfully"
                )
            return ErrorResponseModel(
                "An error occurred", 404, "Image Data with id {0} doesn't exist".format(id)
            )
        else:
            return ErrorResponseModel(
                "An error occurred",
                503,
                "User can't delete Image Data"
            )
    except Exception as e:
        return ErrorResponseModel(
            "An error occurred",
            503,
            e.__str__()
        )
