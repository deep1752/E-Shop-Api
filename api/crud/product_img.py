from sqlalchemy.orm import Session
from api.database.models.product_img import ProductImage
from api.database.schemas.product_img import ProductImageCreate
from typing import List, Dict

def create_product_image(db: Session, product_image: ProductImageCreate):
    for image_url in product_image.images:
        db_image = ProductImage(product_id=product_image.product_id, image=image_url)
        db.add(db_image)
    db.commit()
    return {"product_id": product_image.product_id, "images": product_image.images}

def delete_product_image(db: Session, image_id: int):
    db_image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    if db_image:
        db.delete(db_image)
        db.commit()
    return db_image

# ✅ Get all product images grouped by product_id
def get_all_product_images(db: Session):
    images = db.query(ProductImage).all()
    return images

# ✅ Get images by product_id
def get_product_images_by_product_id(db: Session, product_id: int):
    images = db.query(ProductImage).filter(ProductImage.product_id == product_id).all()
    return images
