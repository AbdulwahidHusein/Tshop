from typing import Optional
from core.config import settings
from bson import ObjectId
from store.schemas.pydantic import StoreCreate, StoreRead

store_collection = settings.DB.get_collection("stores")

async def create_store(store_data: StoreCreate) -> StoreRead:
    store = store_data.model_dump()
    result = await store_collection.insert_one(store)
    store["_id"] = str(result.inserted_id)
    return StoreRead(id=store["_id"], **store)

async def get_store_by_id(store_id: str) -> Optional[StoreRead]:
    store = await store_collection.find_one({"_id": ObjectId(store_id)})
    if store:
        store["_id"] = str(store["_id"])
        return StoreRead(id=store["_id"], **store)
    return None

async def get_store_by_owner_id(owner_id: str) -> Optional[StoreRead]:
    store = await store_collection.find_one({"owner_id": owner_id})
    if store:
        store["_id"] = str(store["_id"])
        return StoreRead(id=store["_id"], **store)
    return None

async def update_store(store_id: str, update_data: dict) -> Optional[StoreRead]:
    update_result = await store_collection.update_one(
        {"_id": ObjectId(store_id)},
        {"$set": update_data}
    )
    if update_result.modified_count > 0:
        store = await store_collection.find_one({"_id": ObjectId(store_id)})
        store["_id"] = str(store["_id"])
        return StoreRead(id=store["_id"], **store)
    return None

async def delete_store(store_id: str) -> bool:
    delete_result = await store_collection.delete_one({"_id": ObjectId(store_id)})
    return delete_result.deleted_count > 0


