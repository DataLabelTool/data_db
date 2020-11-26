from typing import Optional, Union, List, Dict
from bson.objectid import ObjectId
from pydantic import BaseModel, Field


# class PydanticObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
#
#     @classmethod
#     def validate(cls, v):
#         if not isinstance(v, ObjectId):
#             raise TypeError('ObjectId required')
#         return str(v)


class DataSchema(BaseModel):
    data: str = Field(...)
    type: str = Field(...)


class ItemSchema(BaseModel):
    id: str = Field(...)  #PydanticObjectId = Field(...)
    class_name: Optional[str] = Field(...)
    bbox: Optional[DataSchema] = Field(...)
    mask: Optional[DataSchema] = Field(...)

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
    items_graph: Dict[str, List[str]] = Field(...) #Dict[PydanticObjectId, List[PydanticObjectId]] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "image": {"data": "image data", "type": "data_type"},
                "items": [],
                "items_graph": {}
            }
        }


class UpdateImageDataModel(BaseModel):
    image: DataSchema = Field(...)
    items: List[ItemSchema] = Field(...)
    items_graph: Dict[str, List[str]] = Field(...) #Dict[PydanticObjectId, List[PydanticObjectId]] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "image": {"data": "image data", "type": "data_type"},
                "items": [],
                "items_graph": []
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

