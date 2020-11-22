from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder

from src.database.image_data import (
    get_data_ids,
    get_image_data
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


# @image_data_router.get("/", response_description="Image Data ids retrieved")
# async def get_data_ids(
#         db_name: str,
#         task_name: str,
#         user: User = Depends(fastapi_users.get_current_active_user)
# ):
#     """return ids of image_data at specific task"""
#     if user.is_superuser:
#         #TODO: check access to data and if task exists
#         ids = await get_data_ids(db_name, task_name)
#         if ids:
#             return ResponseModel(ids, "Image Data ids retrieved successfully")
#         return ResponseModel([], "Image Data ids are empty")
#     else:
#         return ErrorResponseModel(
#             "An error occurred",
#             503,
#             "There was an error in retrieving Image Data ids."
#         )


@image_data_router.get("/", response_description="Image Data retrieved")
async def get_image_data_route(
        db_name: str,
        task_name: str,
        id: str,
        user: User = Depends(fastapi_users.get_current_active_user)
):
    """return image_data at specific task with id"""
    if user.is_superuser:
        #TODO: check access to data and if task exists
        image_data = await get_image_data(db_name, task_name, id)
        if image_data:
            return ResponseModel(image_data, "Image Data retrieved successfully")
        return ResponseModel({}, "Image Data are empty")
    else:
        return ErrorResponseModel(
            "An error occurred",
            503,
            "There was an error in retrieving Image Data."
        )

#
# @image_data_router.put("/{db_name}.{task_name}.{id}")
# async def update_image_data_route(
#         db_name: str,
#         task_name: str,
#         id: str,
#         req: UpdateImageDataModel = Body(...),
#         user: User = Depends(fastapi_users.get_current_active_user)
# ):
#     """update image data at specific id"""
#     # req = {k: v for k, v in req.dict().items() if v is not None}
#     # updated_student = await update_student(id, req)
#     # if updated_student:
#     #     return ResponseModel(
#     #         "Student with ID: {} name update is successful".format(id),
#     #         "Student name updated successfully",
#     #     )
#     # return ErrorResponseModel(
#     #     "An error occurred",
#     #     404,
#     #     "There was an error updating the student data.",
#     # )


@image_data_router.post("/", response_description="Image Data added into the database")
async def add_image_data_route(
        db_name: str,
        task_name: str,
        id: str,
        image_data: ImageDataSchema = Body(...),
        user: User = Depends(fastapi_users.get_current_active_user)
):
    pass
    # student = jsonable_encoder(student)
    # new_student = await add_student(student)
    # return ResponseModel(new_student, "Student added successfully.")



@image_data_router.delete("/", response_description="Image Data deleted from the database")
async def delete_image_data_route(
        db_name: str,
        task_name: str,
        id: str,
        user: User = Depends(fastapi_users.get_current_active_user)
):
    pass
    # deleted_student = await delete_student(id)
    # if deleted_student:
    #     return ResponseModel(
    #         "Student with ID: {} removed".format(id), "Student deleted successfully"
    #     )
    # return ErrorResponseModel(
    #     "An error occurred", 404, "Student with id {0} doesn't exist".format(id)
    # )
