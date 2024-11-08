from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class StoreCreate(BaseModel):
    telegram_id: Optional[int]
    name: str
    owner_id: str
    description: Optional[str] = None
    additional_fields: Optional[Dict[str, Any]] = None

class StoreRead(BaseModel):
    id: str
    telegram_id: Optional[int]
    name: str
    owner_id: str
    description: Optional[str]
    additional_fields: Optional[Dict[str, Any]]
