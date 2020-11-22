from pydantic import BaseModel, Field
from typing import Dict
from fastapi_users import models



class User(models.BaseUser):
    pass
    # user_level: str = None
    # roles: Dict[str, Dict[str, str]] = Field(...)

    # def can_set_classes(self, db_name: str):
    #     return True
    #
    # def can_set_classes(self, db_name: str):
    #     return True


class UserCreate(models.BaseUserCreate):
    pass
    # roles: Dict[str, Dict[str, str]] = Field(...)


class UserUpdate(User, models.BaseUserUpdate):
    pass
    # roles: Dict[str, Dict[str, str]] = Field(...)


class UserDB(User, models.BaseUserDB):
    pass
    # roles: Dict[str, Dict[str, str]] = Field(...)