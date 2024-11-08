# app/auth/services/auth_service.py
from typing import Optional
from datetime import timedelta
from core.config import settings
from user.schemas.pydantic import UserCreate, UserRead
from bson import ObjectId

user_collection = settings.DB.get_collection("users")


async def create_user(user_data: UserCreate) -> UserRead:
    user = user_data.model_dump()
    result = await user_collection.insert_one(user)
    user["_id"] = str(result.inserted_id)
    return UserRead(**user)


async def get_user_by_tg_id(tg_id: int) -> Optional[UserRead]:
    user = await user_collection.find_one({"tg_id": tg_id})
    if user:
        user["_id"] = str(user["_id"])
        return UserRead(**user)
    return None


async def get_user_by_id(user_id: str) -> Optional[UserRead]:
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return UserRead(**user)
    return None


async def update_user(user_id: str, update_data: dict) -> Optional[UserRead]:
    update_result = await user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )
    if update_result.modified_count > 0:
        user = await user_collection.find_one({"_id": ObjectId(user_id)})
        user["_id"] = str(user["_id"])
        return UserRead(**user)
    return None


async def delete_user(user_id: str) -> bool:
    delete_result = await user_collection.delete_one({"_id": ObjectId(user_id)})
    return delete_result.deleted_count > 0
