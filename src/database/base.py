import os
import motor.motor_asyncio
from bson.objectid import ObjectId
from requests.utils import requote_uri

username = os.getenv('MONGO_ROOT_USER', "devroot")
password = os.getenv('MONGO_ROOT_PASSWORD', 'devroot')
hostname = os.getenv('MONGO_HOST', 'localhost')
port = os.getenv('MONGO_PORT', '62017')
DATABASE_URL = f"mongodb://{requote_uri(username)}:{requote_uri(password)}@{hostname}:{port}"

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
