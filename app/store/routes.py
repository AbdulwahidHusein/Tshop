from fastapi import APIRouter, HTTPException, status
from store.services.store import (
    create_store,
    get_store_by_id,
    update_store,
    delete_store,
    get_store_by_owner_id
)

from store.schemas.pydantic import StoreCreate, StoreRead
from pydantic import BaseModel
from typing import Optional

store_router = APIRouter()

@store_router.post("/stores", response_model=StoreRead, status_code=status.HTTP_201_CREATED)
async def register_store(store_data: StoreCreate):
    """
    Endpoint to create a new store.
    """
    store = await create_store(store_data)
    return store

@store_router.get("/stores/{store_id}", response_model=StoreRead)
async def read_store_by_id(store_id: str):
    """
    Endpoint to get a store by ID.
    """
    store = await get_store_by_id(store_id)
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")
    return store

@store_router.get("/stores/user/{user_id}", response_model=StoreRead)
async def get_user_stores(user_id: str):
    """
    Endpoint to get stores by user ID.
    """
    store = await get_store_by_owner_id(user_id)
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No stores found for this user")
    return store

class StoreUpdateRequest(BaseModel):
    name: Optional[str] = None
    owner_id: Optional[int] = None
    description: Optional[str] = None
    telegram_id: Optional[int] = None
    additional_fields: Optional[dict] = None

@store_router.put("/stores/{store_id}", response_model=StoreRead)
async def update_store_data(store_id: str, update_data: StoreUpdateRequest):
    """
    Endpoint to update a store's information.
    """
    updated_store = await update_store(store_id, update_data.dict(exclude_unset=True))
    if not updated_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found or no updates made")
    return updated_store

@store_router.delete("/stores/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_store_data(store_id: str):
    """
    Endpoint to delete a store.
    """
    deleted = await delete_store(store_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")
    return {"message": "Store deleted successfully"}
