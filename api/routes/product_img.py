from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.database.schemas.product_img import ProductImageResponse, ProductImageCreate
from api.crud.product_img import create_product_image, delete_product_image, get_all_product_images, get_product_images_by_product_id
from typing import List, Optional

router = APIRouter()

@router.post("/", response_model=ProductImageResponse)
def create_image(image: ProductImageCreate, db: Session = Depends(get_db)):
    return create_product_image(db, image)


@router.delete("/{image_id}", response_model=ProductImageResponse)
def delete_image(image_id: int, db: Session = Depends(get_db)):
    image = delete_product_image(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image


@router.get("/", response_model=List[ProductImageResponse])
def get_images(product_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Get all product images or filter by product_id
    """
    if product_id:
        images = get_product_images_by_product_id(db, product_id)
        if not images:
            raise HTTPException(status_code=404, detail="No images found for this product_id")
    else:
        images = get_all_product_images(db)
        if not images:
            raise HTTPException(status_code=404, detail="No images found")

    # Group images by product_id
    grouped_images = {}
    for img in images:
        if img.product_id not in grouped_images:
            grouped_images[img.product_id] = []
        grouped_images[img.product_id].append(img.image)

    return [{"id": product_id, "product_id": product_id, "images": imgs} for product_id, imgs in grouped_images.items()]
