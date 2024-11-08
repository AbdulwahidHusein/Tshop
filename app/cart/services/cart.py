from typing import Optional, List
from bson import ObjectId
from core.config import settings
from cart.schemas.pydantic import CartCreate, CartRead, CartItemCreate, CartItemRead

cart_collection = settings.DB.get_collection("carts")
cart_item_collection = settings.DB.get_collection("cart_items")

# Cart Services
async def create_cart(cart_data: CartCreate) -> CartRead:
    cart = cart_data.model_dump()
    result = await cart_collection.insert_one(cart)
    cart["_id"] = str(result.inserted_id)
    return CartRead(id=cart["_id"], **cart)

async def get_cart_by_user_id(user_id: str) -> Optional[CartRead]:
    cart = await cart_collection.find_one({"user_id": ObjectId(user_id)})
    if cart:
        cart["_id"] = str(cart["_id"])
        return CartRead(id=cart["_id"], **cart)
    return None

async def delete_cart(cart_id: str) -> bool:
    delete_result = await cart_collection.delete_one({"_id": ObjectId(cart_id)})
    return delete_result.deleted_count > 0

# Cart Item Services
async def add_item_to_cart(cart_item_data: CartItemCreate) -> CartItemRead:
    item = cart_item_data.model_dump()
    result = await cart_item_collection.insert_one(item)
    item["_id"] = str(result.inserted_id)
    return CartItemRead(id=item["_id"], **item)

async def get_items_by_cart_id(cart_id: str) -> List[CartItemRead]:
    items = cart_item_collection.find({"cart_id": ObjectId(cart_id)})
    return [CartItemRead(id=str(item["_id"]), **item) async for item in items]

async def update_cart_item(cart_item_id: str, update_data: dict) -> Optional[CartItemRead]:
    update_result = await cart_item_collection.update_one(
        {"_id": ObjectId(cart_item_id)}, {"$set": update_data}
    )
    if update_result.modified_count > 0:
        item = await cart_item_collection.find_one({"_id": ObjectId(cart_item_id)})
        item["_id"] = str(item["_id"])
        return CartItemRead(id=item["_id"], **item)
    return None

async def delete_cart_item(cart_item_id: str) -> bool:
    delete_result = await cart_item_collection.delete_one({"_id": ObjectId(cart_item_id)})
    return delete_result.deleted_count > 0
