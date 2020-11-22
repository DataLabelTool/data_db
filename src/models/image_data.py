from typing import Optional, Union, List
from pydantic import BaseModel, EmailStr, Field


class DataSchema(BaseModel):
    data: str = Field(...)
    type: str = Field(...)


class ItemSchema(BaseModel):
    class_name: Optional[str] = Field(...)
    bbox: Optional[DataSchema] = Field(...)
    mask: Optional[DataSchema] = Field(...)
    childs: Optional[List] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "class_name": "label1",
                "bbox": {"data": "data", "type": "bbox type"},
                "mask": {"data": "data", "type": "bbox type"},
            }
        }


class ImageDataSchema(BaseModel):
    image: DataSchema = Field(...)
    items: List[ItemSchema] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "image": {"data": "image data", "type": "data_type"},
                "items": [],
            }
        }


class UpdateImageDataModel(BaseModel):
    image: DataSchema = Field(...)
    items: List[ItemSchema] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "image": {"data": "image data", "type": "data_type"},
                "items": [],
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

