from fastapi import APIRouter, HTTPException, status
from typing import List
from product.services.product import (
    create_product,
    get_product_by_id,
    get_products_by_tg_group_id,
    update_product,
    delete_product
)
from product.schemas.pydantic import ProductCreate, ProductRead
from pydantic import BaseModel
from typing import Optional

product_router = APIRouter()

@product_router.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def register_product(product_data: ProductCreate):
    """
    Endpoint to create a new product.
    """
    product = await create_product(product_data)
    return product

@product_router.get("/products/{product_id}", response_model=ProductRead)
async def read_product_by_id(product_id: str):
    """
    Endpoint to get a product by ID.
    """
    product = await get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@product_router.get("/products/tg_group/{tg_group_id}", response_model=List[ProductRead])
async def read_products_by_tg_group(tg_group_id: int):
    """
    Endpoint to get all products for a specific tg group.
    """
    products = await get_products_by_tg_group_id(tg_group_id)
    return products

class ProductUpdateRequest(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    additional_fields: Optional[dict] = None

@product_router.put("/products/{product_id}", response_model=ProductRead)
async def update_product_data(product_id: str, update_data: ProductUpdateRequest):
    """
    Endpoint to update a product's information.
    """
    updated_product = await update_product(product_id, update_data.dict(exclude_unset=True))
    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or no updates made")
    return updated_product

@product_router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_data(product_id: str):
    """
    Endpoint to delete a product.
    """
    deleted = await delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {"message": "Product deleted successfully"}
