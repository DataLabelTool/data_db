from typing import List
from pydantic import BaseModel, Field


class TaskSchema(BaseModel):
    db_name: str = Field(...)
    task_names: List[str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "db_name": "data_db",
                "task_names": ["task1", "task2"]
            }
        }


class DBSchema(BaseModel):
    db_names: List[TaskSchema] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "db_names": [
                    {
                        "db_name": "data_db",
                        "task_names": ["task1", "task2"]
                    }
                ]
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

