from bson.objectid import ObjectId
from src.database.base import client


# Get data ids
async def get_data_ids(db_name: str, task_name: str):
    database = client[db_name]
    cursor = database.get_collection(task_name).find({}, {'_id': 1})
    data_ids = list(cursor)
    return data_ids


# Get image data with specific id
async def get_image_data(db_name: str, task_name: str, id: str) -> dict:
    database = client[db_name]
    image_data = await database.get_collection(task_name).find_one({"_id": ObjectId(id)})
    if image_data:
        return image_data_helper(image_data)


# Update image_data with a matching ID
async def update_image_data(db_name: str, task_name: str, id: str, data: dict, check_protected: bool = False):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    database = client[db_name]
    image_data_collection = database.get_collection(task_name)
    image_data_left = await image_data_collection.find_one({'_id': ObjectId(id)})
    if image_data_left is not None:
        if not check_protected or image_data_check_protected(image_data_left, data):
            updated_image_data = await image_data_collection.update_one(
                {'_id': ObjectId(id)}, {"$set": data}
            )
        else:
            return False
    else:
        updated_image_data = image_data_collection.insert_one(data)

    if updated_image_data:
        return True
    return False


# Add a new student into to the database
async def add_image_data(db_name: str, task_name: str, image_data: dict) -> dict:
    database = client[db_name]
    image_data_collection = database.get_collection(task_name)
    image_data_cursor = await image_data_collection.insert_one(image_data)
    new_image_data = await image_data_collection.find_one({"_id": image_data_cursor.inserted_id})
    return image_data_helper(new_image_data)


# Delete a student from the database
async def delete_image_data(db_name: str, task_name: str, id: str):
    database = client[db_name]
    image_data_collection = database.get_collection(task_name)
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True



def image_data_helper(image_data_dict: dict) -> dict:
    data = {
        "id": str(image_data_dict["_id"]),
        "image": image_data_dict["image"],
        "items": image_data_dict["items"]
    }
    #TODO: check other keys
    return data

def image_data_check_protected(image_data_dict_left: dict, image_data_dict_right: dict) -> bool:
    """check"""

    #TODO: impelement method
    return True
