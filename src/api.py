import requests
from fastapi import FastAPI
from src.version import version
from src.utils import project_root, base_url

from src.database.users import create_first_admin

from src.routes.users import (
    jwt_auth_router,
    register_router,
    reset_password_router,
    users_router
)
from src.routes.classes import classes_router
from src.routes.image_data import image_data_router
from src.routes.tasks import tasks_router, dbs_router

app = FastAPI(
    title="data_db",
    version=version,
    root_path=requests.utils.urlparse(base_url()).path
)

@app.on_event("startup")
async def create_db_client():
    # start client here and reuse in future requests
    success = await create_first_admin()

@app.on_event("shutdown")
async def shutdown_db_client():
    # stop your client here
    pass

# classes routes
app.include_router(
    classes_router,
    prefix="/classes"
)

# image data routes
app.include_router(image_data_router, prefix="/image_data")
# tasks data routes
app.include_router(tasks_router, prefix="/tasks")
# dbs data routes
app.include_router(dbs_router, prefix="/dbs")


# users routers
app.include_router(jwt_auth_router, prefix="/auth/jwt", tags=["auth"])
app.include_router(register_router, prefix="/auth", tags=["auth"])
# app.include_router(reset_password_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])

"""
uvicorn src.api:app --port 8081 --host 0.0.0.0 --reload
"""