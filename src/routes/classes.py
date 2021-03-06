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


@classes_router.post("/", response_description="Classes data added into the database")
async def set_classes_data(
        db_name: str,
        classes: List[ClassSchema] = Body(...),
        user: User = Depends(fastapi_users.get_current_active_user)
):
    try:
        if user.can_set_classes(db_name=db_name):
            classes = jsonable_encoder(classes)
            new_classes = await set_classes(classes, db_name)
            print("new_classes", new_classes)
            if new_classes:
                return ResponseModel(new_classes, "Classes added successfully.")
            else:
                return ErrorResponseModel(
                    "An error occurred",
                    404,
                    "Can't set classes for this db"
                )
        else:
            return ErrorResponseModel(
                "An error occurred",
                503,
                "User does not have admin privilegies",
            )
    except Exception as e:
        return ErrorResponseModel(
            "An error occurred",
            503,
            e.__str__()
        )


@classes_router.get("/", response_description="Classes data retrieved")
async def get_classes_data(
        db_name: str,
        user: User = Depends(fastapi_users.get_current_active_user)
) -> ResponseModel:
    try:
        if user.can_get_classes(db_name=db_name):
            classes = await get_classes(db_name=db_name)
            if classes:
                return ResponseModel(classes, "Classes data retrieved successfully")
            else:
                return ErrorResponseModel(
                    "An error occurred",
                    404,
                    "Can't get classes for this db"
                )
        else:
            return ErrorResponseModel(
                "An error occurred",
                503,
                "User does not have admin privilegies",
            )
    except Exception as e:
        return ErrorResponseModel(
            "An error occurred",
            503,
            e.__str__()
        )
