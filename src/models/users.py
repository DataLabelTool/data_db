from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from fastapi_users import models


class User(models.BaseUser):

    roles_db: List[str] = Field(
        default=[],
        description="roles in db: add, delete"
    )
    roles_tasks: Dict[str, List[str]] = Field(
        default={},
        description="roles in db task: add, delete"
    )
    roles_classes: Dict[str, List[str]] = Field(
        default={},
        description="roles in db classes: set, get"
    )
    roles_image_data: Dict[str, Dict[str, List[str]]] = Field(
        default={},
        description="roles in db tasks with image_data: get, edit, edit_protected, add, delete"
    )

    # dbs
    def can_add_dbs(self):
        if self.is_superuser:
            return True
        else:
            if 'can_add' in self.roles_db:
                return True
            else:
                return False

    def can_delete_dbs(self):
        if self.is_superuser:
            return True
        else:
            if 'can_delete' in self.roles_db:
                return True
            else:
                return False

    # tasks
    def can_add_tasks(self, db_name: str):
        if self.is_superuser:
            return True
        else:
            roles = self.roles_tasks.get(db_name, [])
            if len(roles) > 0 and 'can_add' in roles:
                return True
            else:
                return False

    def can_delete_tasks(self, db_name: str):
        if self.is_superuser:
            return True
        else:
            roles = self.roles_tasks.get(db_name, [])
            if len(roles) > 0 and 'can_delete' in roles:
                return True
            else:
                return False

    # classes
    def can_get_classes(self, db_name: str):
        if self.is_superuser:
            return True
        else:
            roles = self.roles_classes.get(db_name, [])
            if len(roles) > 0 and 'can_get' in roles:
                return True
            else:
                return False

    def can_set_classes(self, db_name: str):
        if self.is_superuser:
            return True
        else:
            roles = self.roles_classes.get(db_name, [])
            if len(roles) > 0 and 'can_set' in roles:
                return True
            else:
                return False

    # image_data
    def can_get_image_data(self, db_name: str, task_name: str):
        if self.is_superuser:
            return True
        else:
            roles_db_lvl = self.roles_image_data.get(db_name, {})
            if len(roles_db_lvl) > 0:
                roles_task_lvl = roles_db_lvl.get(task_name, [])
                if len(roles_task_lvl) and 'can_get' in roles_task_lvl:
                    return True
                else:
                    return False
            else:
                return False

    def can_edit_image_data(self, db_name: str, task_name: str):
        if self.is_superuser:
            return True
        else:
            roles_db_lvl = self.roles_image_data.get(db_name, {})
            if len(roles_db_lvl) > 0:
                roles_task_lvl = roles_db_lvl.get(task_name, [])
                if len(roles_task_lvl) and 'can_edit' in roles_task_lvl:
                    return True
                else:
                    return False
            else:
                return False

    def can_edit_protected_image_data(self, db_name: str, task_name: str):
        if self.is_superuser:
            return True
        else:
            roles_db_lvl = self.roles_image_data.get(db_name, {})
            if len(roles_db_lvl) > 0:
                roles_task_lvl = roles_db_lvl.get(task_name, [])
                if len(roles_task_lvl) and 'can_edit_protected' in roles_task_lvl:
                    return True
                else:
                    return False
            else:
                return False

    def can_add_image_data(self, db_name: str, task_name: str):
        if self.is_superuser:
            return True
        else:
            roles_db_lvl = self.roles_image_data.get(db_name, {})
            if len(roles_db_lvl) > 0:
                roles_task_lvl = roles_db_lvl.get(task_name, [])
                if len(roles_task_lvl) and 'can_add' in roles_task_lvl:
                    return True
                else:
                    return False
            else:
                return False

    def can_delete_image_data(self, db_name: str, task_name: str):
        if self.is_superuser:
            return True
        else:
            roles_db_lvl = self.roles_image_data.get(db_name, {})
            if len(roles_db_lvl) > 0:
                roles_task_lvl = roles_db_lvl.get(task_name, [])
                if len(roles_task_lvl) and 'can_delete' in roles_task_lvl:
                    return True
                else:
                    return False
            else:
                return False


class UserCreate(models.BaseUserCreate):

    def create_update_dict(self):
        return self.dict(
            exclude_unset=True,
            exclude={
                "id", "is_superuser", "is_active", "oauth_accounts",
                "roles_db", "roles_tasks", "roles_classes", "roles_image_data"
            },
        )


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass