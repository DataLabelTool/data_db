import os
import requests
from typing import Dict, Any, cast, Optional
from src.utils import base_url
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.password import get_password_hash
from fastapi_users import FastAPIUsers
from pydantic import UUID4, EmailStr
from fastapi import Request, Response, Depends, HTTPException, status, APIRouter

SECRET = os.getenv('API_SECRET', "SECRET")

from src.database.users import user_db

from src.models.users import (
    User,
    UserDB,
    UserCreate,
    UserUpdate,
)


def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    # todo: send email to user with token
    print(f"User {user.id} has forgot their password. Reset token: {token}")


jwt_authentication = JWTAuthentication(
    secret=SECRET,
    lifetime_seconds=3600,
    tokenUrl=requests.utils.urlparse(base_url()).path + "/auth/jwt/login"
)

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

jwt_auth_router = fastapi_users.get_auth_router(jwt_authentication)

@jwt_auth_router.post("/auth/jwt/refresh")
async def refresh_jwt(response: Response, user=Depends(fastapi_users.get_current_active_user)):
    return await jwt_authentication.get_login_response(user, response)

register_router = fastapi_users.get_register_router(on_after_register)

reset_password_router = fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password
)

# users_router = fastapi_users.get_users_router()
users_router = APIRouter()


async def _get_or_404(id: UUID4) -> UserDB:
    user = await user_db.get(id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


async def _update_user(
    user: UserDB, update_dict: Dict[str, Any], request: Request
):
    #TODO: implement changing roles
    for field in update_dict:
        if field == "password":
            hashed_password = get_password_hash(update_dict[field])
            user.hashed_password = hashed_password
        else:
            setattr(user, field, update_dict[field])
    updated_user = await user_db.update(user)
    return updated_user


@users_router.get("/me", response_model=User)
async def me(
    user: User = Depends(fastapi_users.get_current_active_user),  # type: ignore
):
    return user


@users_router.patch("/me", response_model=User)
async def update_me(
    request: Request,
    updated_user: UserUpdate,  # type: ignore
    user: User = Depends(fastapi_users.get_current_active_user),  # type: ignore
):
    updated_user_data = updated_user.create_update_dict()
    updated_user = await _update_user(user, updated_user_data, request)

    return updated_user


# superuser routes
@users_router.get(
    "/",
    response_model=User,
    dependencies=[Depends(fastapi_users.get_current_superuser)],
)
async def get_user(
        id: Optional[UUID4] = None,
        email: Optional[EmailStr] = None
):
    if id is not None:
        return await _get_or_404(id)
    elif email is not None:
        user = await user_db.get_by_email(email=email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@users_router.patch(
    "/",
    response_model=User,
    dependencies=[Depends(fastapi_users.get_current_superuser)],
)
async def update_user(
    id: UUID4, updated_user: UserUpdate, request: Request  # type: ignore
):
    updated_user = cast(
        UserUpdate,
        updated_user,
    )  # Prevent mypy complain
    user = await _get_or_404(id)
    updated_user_data = updated_user.create_update_dict_superuser()
    return await _update_user(user, updated_user_data, request)

@users_router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(fastapi_users.get_current_superuser)],
)
async def delete_user(id: UUID4):
    user = await _get_or_404(id)
    await user_db.delete(user)
    return None

