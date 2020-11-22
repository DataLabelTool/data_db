from typing import List
from pydantic import BaseModel, Field


class ClassSchema(BaseModel):
    class_name: str = Field(...)
    mask_color: List[int] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "class_name": "label",
                "mask_color": [0, 0, 128, 255]
            }
        }


def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }