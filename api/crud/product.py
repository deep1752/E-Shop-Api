from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from api.database.models.products import Products
from api.database.models.categories import Categories
from api.database.schemas.products import ProductsCreate, ProductsUpdate
from datetime import datetime
from typing import List, Optional
from slugify import slugify

def create_product(db: Session, product: ProductsCreate):
    created_at = product.created_at or datetime.utcnow()
    updated_at = product.updated_at or datetime.utcnow()

    db_product = Products(
        category_id=product.category_id,
        name=product.name,
        slug=slugify(product.name),
        description=product.description,
        mrp=product.mrp,
        net_price=product.net_price,
        quantity_in_stock=product.quantity_in_stock,
        image=product.image,
        product_cat=product.product_cat,
        created_at=created_at,
        updated_at=updated_at,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_data: ProductsUpdate):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_data.dict(exclude_unset=True)
    if "name" in update_data:
        update_data["slug"] = slugify(update_data["name"])

    for key, value in update_data.items():
        setattr(product, key, value)

    product.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(product)
    return product

def bulk_add_products(db: Session, products: List[ProductsCreate]) -> List[Products]:
    created_products = []
    for product in products:
        created = create_product(db, product)
        created_products.append(created)
    return created_products

def delete_product(db: Session, product_id: int):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"success": True, "message": "Product deleted successfully"}

def get_product_by_id(db: Session, slug: str):
    return db.query(Products).filter(Products.slug == slug).first()

def get_product_by_ids(db: Session, product_id: int):
    return db.query(Products).filter(Products.id == product_id).first()

def get_all_products(db: Session, category: Optional[str] = None):
    query = db.query(Products).options(joinedload(Products.category))
    if category:
        query = query.filter(Products.product_cat == category)

    products = query.all()
    result = []
    for product in products:
        product_data = product.__dict__.copy()
        product_data["category_name"] = product.category.name if product.category else None
        result.append(product_data)
    return result
