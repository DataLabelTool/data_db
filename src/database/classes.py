from src.database.base import client
from src.models.classes import ClassSchema
from typing import List


def class_helper(class_dict) -> dict:

    return {
        "class_name": class_dict["class_name"],
        "mask_color": class_dict["mask_color"]
    }


async def get_classes(db_name: str) -> List[dict]:
    """
    Get classes for db db_name
    :param db_name:
    :return:
    """
    database = client[db_name]
    classes_collection = database.get_collection("classes")
    classes = []
    async for class_inst in classes_collection.find():
        classes.append(class_helper(class_inst))
    return classes


# Add a new classes into to the database
async def set_classes(classes_data: List[ClassSchema], db_name: str) -> List[str]:
    database = client[db_name]
    classes_collection = database.get_collection("classes")
    num_documents = await classes_collection.count_documents({})
    if num_documents > 0:
        result = await classes_collection.drop()
        result = await classes_collection.insert_many(classes_data)
    else:
        result = await classes_collection.insert_many(classes_data)
    return [str(id) for id in result.inserted_ids]

