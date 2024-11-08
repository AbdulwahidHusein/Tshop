from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ProductCreate(BaseModel):
    tg_group_id:int
    store_id: str
    name: str
    price: float
    description: Optional[str] = None
    additional_fields: Optional[Dict[str, Any]] = None

class ProductRead(BaseModel):
    id: str
    tg_group_id: int
    store_id: str
    name: str
    price: float
    description: Optional[str]
    additional_fields: Optional[Dict[str, Any]]
