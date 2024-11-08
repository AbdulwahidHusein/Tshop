from fastapi import APIRouter, HTTPException, Depends
from cart.schemas.pydantic import CartCreate, CartRead, CartItemCreate, CartItemRead
from typing import List
from cart.services.cart import (
    create_cart,
    get_cart_by_user_id,
    delete_cart,
    add_item_to_cart,
    get_items_by_cart_id,
    update_cart_item,
    delete_cart_item,
)

cart_router = APIRouter()

# Cart Routes
@cart_router.post("/carts/", response_model=CartRead)
async def create_new_cart(cart: CartCreate):
    return await create_cart(cart)

@cart_router.get("/carts/{user_id}", response_model=CartRead)
async def get_cart(user_id: str):
    cart = await get_cart_by_user_id(user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

@cart_router.delete("/carts/{cart_id}", status_code=204)
async def remove_cart(cart_id: str):
    if not await delete_cart(cart_id):
        raise HTTPException(status_code=404, detail="Cart not found")

# Cart Item Routes
@cart_router.post("/cart-items/", response_model=CartItemRead)
async def add_item(cart_item: CartItemCreate):
    return await add_item_to_cart(cart_item)

@cart_router.get("/cart-items/{cart_id}", response_model=List[CartItemRead])
async def get_cart_items(cart_id: str):
    return await get_items_by_cart_id(cart_id)

@cart_router.patch("/cart-items/{item_id}", response_model=CartItemRead)
async def modify_cart_item(item_id: str, update_data: dict):
    updated_item = await update_cart_item(item_id, update_data)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return updated_item

@cart_router.delete("/cart-items/{item_id}", status_code=204)
async def remove_cart_item(item_id: str):
    if not await delete_cart_item(item_id):
        raise HTTPException(status_code=404, detail="Cart item not found")
