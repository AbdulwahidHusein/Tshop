from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

# Pydantic model for Cart schema
class CartBase(BaseModel):
    user_id: str
    additional_fields: Optional[Dict[str, Any]] = None

class CartCreate(CartBase):
    pass

class CartRead(CartBase):
    id: str

class CartItemBase(BaseModel):
    cart_id: str
    product_id: str
    quantity: Optional[int] = 1
    additional_fields: Optional[Dict[str, Any]] = None

class CartItemCreate(CartItemBase):
    pass

class CartItemRead(CartItemBase):
    id: str
