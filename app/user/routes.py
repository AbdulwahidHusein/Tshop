# app/auth/routes.py

from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from user.services.user import (
    create_user,
    get_user_by_tg_id,
    get_user_by_id,
    update_user,
    delete_user
)

from user.schemas.pydantic import UserCreate, UserRead
from pydantic import BaseModel

user_router = APIRouter()

@user_router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    """
    Endpoint to create a new user.
    """
    user = await create_user(user_data)
    return user

@user_router.get("/users/{user_id}", response_model=UserRead)
async def read_user_by_id(user_id: str):
    """
    Endpoint to get a user by ID.
    """
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@user_router.get("/users/tg_id/{tg_id}", response_model=UserRead)
async def read_user_by_tg_id(tg_id: int):
    """
    Endpoint to get a user by Telegram ID.
    """
    user = await get_user_by_tg_id(tg_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

class UserUpdateRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    # tg_id: Optional[int] = None
    additional_fields: Optional[dict] = None

@user_router.put("/users/{user_id}", response_model=UserRead)
async def update_user_data(user_id: str, update_data: UserUpdateRequest):
    """
    Endpoint to update a user's information.
    """
    updated_user = await update_user(user_id, update_data.dict(exclude_unset=True))
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or no updates made")
    return updated_user

@user_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_data(user_id: str):
    """
    Endpoint to delete a user.
    """
    deleted = await delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User deleted successfully"}
