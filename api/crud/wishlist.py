from sqlalchemy.orm import Session
from api.database.models.wishlist import Wishlist
from api.database.schemas.wishlist import WishlistCreate
from fastapi import HTTPException

def create_wishlist_item(db: Session, wishlist: WishlistCreate):
    # Check for duplicates
    existing_item = db.query(Wishlist).filter_by(
        user_id=wishlist.user_id, product_id=wishlist.product_id
    ).first()

    if existing_item:
        raise HTTPException(status_code=400, detail="Item already in wishlist")

    db_item = Wishlist(**wishlist.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_all_wishlist_items(db: Session):
    return db.query(Wishlist).all()

def get_user_wishlist(db: Session, user_id: int):
    return db.query(Wishlist).filter(Wishlist.user_id == user_id).all()
