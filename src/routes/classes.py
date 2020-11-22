from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from typing import List

from src.database.classes import (
    set_classes,
    get_classes,
)
from src.models.classes import (
    ErrorResponseModel,
    ResponseModel,
    ClassSchema
)
from src.models.users import User
from src.routes.users import fastapi_users


classes_router = APIRouter()


@classes_router.post("/{db_name}", response_description="Classes data added into the database")
async def set_classes_data(
        db_name: str,
        classes: List[ClassSchema] = Body(...),
        user: User = Depends(fastapi_users.get_current_active_user)
):
    if not user.is_superuser:
        ErrorResponseModel(
            "An error occurred",
            503,
            "User does not have admin privilegies",
        )
    else:
        classes = jsonable_encoder(classes)
        new_classes = await set_classes(classes, db_name)
        return ResponseModel(new_classes, "Classes added successfully.")


@classes_router.get("/{db_name}", response_description="Classes data retrieved")
async def get_classes_data(
        db_name: str,
        user: User = Depends(fastapi_users.get_current_user)
) -> ResponseModel:

    if user.is_superuser:
        ErrorResponseModel(
            "An error occurred",
            503,
            "User does not have admin privilegies",
        )
    else:
        classes = await get_classes(db_name=db_name)
        if classes:
            return ResponseModel(classes, "Classes data retrieved successfully")
    return ErrorResponseModel("An error occurred", 404, "db_name {0} doesn't exist".format(id))