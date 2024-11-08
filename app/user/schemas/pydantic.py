# app/auth/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    tg_id: Optional[int] = None
    additional_fields: Optional[dict] = None

class UserCreate(UserBase):
    pass  

class UserRead(UserBase):
    id: str = Field(..., alias="_id")

class UserLogin(BaseModel):
    username: str
    password: str
