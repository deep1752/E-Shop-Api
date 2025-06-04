from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductsCreate(BaseModel):
    category_id: int
    name: str 
    description: str
    mrp: float
    net_price: float
    quantity_in_stock: int
    image: str
    product_cat: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ProductsUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    mrp: Optional[float] = None
    net_price: Optional[float] = None
    quantity_in_stock: Optional[int] = None
    image: Optional[str] = None
    product_cat: Optional[str] = None

class ProductsResponse(BaseModel):
    id: int
    category_id: int
    name: str
    slug: Optional[str] = None
    description: str
    mrp: float
    net_price: float
    quantity_in_stock: int
    image: str
    product_cat: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProductWithCategory(BaseModel):
    id: int
    category_name: Optional[str]
    name: str
    slug: Optional[str] = None
    description: str
    mrp: float
    net_price: float
    quantity_in_stock: int
    image: str
    product_cat: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
