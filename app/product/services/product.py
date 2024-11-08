from typing import Optional, List
from core.config import settings
from bson import ObjectId
from product.schemas.pydantic import ProductCreate, ProductRead

product_collection = settings.DB.get_collection("products")

async def create_product(product_data: ProductCreate) -> ProductRead:
    product = product_data.model_dump()
    result = await product_collection.insert_one(product)
    product["_id"] = str(result.inserted_id)
    return ProductRead(id=product["_id"], **product)

async def get_product_by_id(product_id: str) -> Optional[ProductRead]:
    product = await product_collection.find_one({"_id": ObjectId(product_id)})
    if product:
        product["_id"] = str(product["_id"])
        return ProductRead(id=product["_id"], **product)
    return None

async def get_products_by_store(store_id: str) -> List[ProductRead]:
    products = await product_collection.find({"store_id": store_id}).to_list(None)
    return [ProductRead(id=str(product["_id"]), **product) for product in products]

async def get_products_by_tg_group_id(tg_group_id: int) -> List[ProductRead]:
    products = await product_collection.find({"tg_group_id": tg_group_id}).to_list(None)
    return [ProductRead(id=str(product["_id"]), **product) for product in products]


async def update_product(product_id: str, update_data: dict) -> Optional[ProductRead]:
    update_result = await product_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )
    if update_result.modified_count > 0:
        product = await product_collection.find_one({"_id": ObjectId(product_id)})
        product["_id"] = str(product["_id"])
        return ProductRead(id=product["_id"], **product)
    return None

async def delete_product(product_id: str) -> bool:
    delete_result = await product_collection.delete_one({"_id": ObjectId(product_id)})
    return delete_result.deleted_count > 0
