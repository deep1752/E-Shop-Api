from pydantic import BaseModel
from typing import List

# ✅ Schema
class ProductImageBase(BaseModel):
    product_id: int
    images: List[str]  # Ensures we return a list of images per product

class ProductImageCreate(ProductImageBase):
    pass

class ProductImageResponse(ProductImageBase):
    id: int
    class Config:
        from_attributes = True
