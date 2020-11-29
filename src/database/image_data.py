from bson.objectid import ObjectId
from src.database.base import client
from src.database.tasks import get_dbs, get_db_tasks


restricted_keys = ['items_state', 'predicted_items']


async def check_task_exist(db_name: str, task_name: str):
    db_tasks = await get_db_tasks()
    db_names = [db_tasks_name.db_name for db_tasks_name in db_tasks]
    assert db_name in db_names, "DB does not exist"
    task_names = [db_task.task_names for db_task in db_tasks if db_task.db_name == db_name][0]
    assert task_name in task_names, "Task does not exist"

# Get data ids
async def get_image_data_ids(db_name: str, task_name: str):
    await check_task_exist(db_name, task_name)
    database = client[db_name]
    cursor = database[task_name].find({}, {'_id': 1})
    data_ids = []
    async for data_id in cursor:
        data_ids.append(image_data_id_helper(data_id))
    return data_ids


# Get image data with specific id
async def get_image_data(db_name: str, task_name: str, id: str) -> dict:
    await check_task_exist(db_name, task_name)
    database = client[db_name]
    image_data = await database[task_name].find_one({"_id": ObjectId(id)})
    if image_data:
        return image_data_helper(image_data)


# Update image_data with a matching ID
async def update_image_data(db_name: str, task_name: str, id: str, image_data: dict, check_protected: bool = False):
    # Return false if an empty request body is sent.
    if len(image_data) < 1:
        return False
    await check_task_exist(db_name, task_name)

    database = client[db_name]
    image_data_collection = database[task_name]
    image_data_left = await image_data_collection.find_one({'_id': ObjectId(id)})
    if image_data_left is not None:
        if not check_protected or image_data_check_protected(image_data_left, image_data):
            updated_image_data = await image_data_collection.update_one(
                {'_id': ObjectId(id)}, {"$set": image_data}
            )
        else:
            return False
    else:
        updated_image_data = image_data_collection.insert_one(image_data)

    if updated_image_data:
        return True
    return False


# Add a new image data into to the database
async def add_image_data(db_name: str, task_name: str, image_data: dict) -> dict:
    await check_task_exist(db_name, task_name)
    database = client[db_name]
    image_data_collection = database[task_name]
    image_data_cursor = await image_data_collection.insert_one(image_data)
    new_image_data = await image_data_collection.find_one({"_id": image_data_cursor.inserted_id})
    return image_data_helper(new_image_data)


# Delete a image data from the database
async def delete_image_data(db_name: str, task_name: str, id: str):
    await check_task_exist(db_name, task_name)
    database = client[db_name]
    image_data_collection = database[task_name]
    image_data = await image_data_collection.find_one({"_id": ObjectId(id)}, {'_id': 1})
    if image_data:
        await image_data_collection.delete_one({"_id": ObjectId(id)})
        return True
    else:
        return False


def image_data_id_helper(image_data_dict: dict) -> dict:
    data = {
        "_id": str(image_data_dict["_id"])
    }
    return data


def image_data_helper(image_data_dict: dict) -> dict:
    data = {
        "_id": str(image_data_dict["_id"]),
        "image": image_data_dict["image"],
        "items": image_data_dict["items"],
        "items_graph": image_data_dict["items_graph"]
    }
    for key, val in image_data_dict.items():
        if key not in restricted_keys:
            data[key] = val
    return data


def image_data_check_protected(image_data_dict_left: dict, image_data_dict_right: dict) -> bool:
    """check"""
    main_keys = ["_id", "image"]
    for key in main_keys:
        assert image_data_dict_left[key] == image_data_dict_right[key], "Keys are not equal with key: " + key
    # check protected in items
    left_items = [item for item in image_data_dict_left["items"] if item.get("protected", False)]
    right_items = [item for item in image_data_dict_right["items"] if item.get("protected", False)]
    for left in left_items:
        left_id = left.get("id", None)
        if left_id:
            right_items_with_id = [right for right in right_items if right.get("id", None) == left_id]

            for right in right_items_with_id:
                assert left == right, "Protected items are changed id: " + right.get("id")
    # check protected in items_graph
    # TODO: now check items_graph not implemented
    # check other keys
    # TODO: now we are not need to check other keys
    return True
