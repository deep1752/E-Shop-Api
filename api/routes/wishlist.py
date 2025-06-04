from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.database.schemas.wishlist import WishlistCreate, WishlistResponse,WishlistRemove
from api.database.models.wishlist import Wishlist
from api.crud import wishlist as crud
from api.database.connection import get_db

router = APIRouter()

@router.post("/add", response_model=WishlistResponse)
def add_to_wishlist(wishlist: WishlistCreate, db: Session = Depends(get_db)):
    return crud.create_wishlist_item(db, wishlist)

@router.get("/get", response_model=List[WishlistResponse])
def get_all_wishlist_items(db: Session = Depends(get_db)):
    return crud.get_all_wishlist_items(db)

@router.get("/user/{user_id}", response_model=List[WishlistResponse])
def get_user_wishlist(user_id: int, db: Session = Depends(get_db)):
    items = crud.get_user_wishlist(db, user_id)
    if not items:
        return []  # Return an empty list if no wishlist items are found
    return items

@router.delete("/delete/{wishlist_id}")
def delete_wishlist_item(wishlist_id: int, db: Session = Depends(get_db)):
    item = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"detail": "Item removed from wishlist"}


@router.delete("/wishlist/delete")
def remove_wishlist_item(payload: WishlistRemove, db: Session = Depends(get_db)):
    wishlist_item = db.query(Wishlist).filter_by(
        user_id=payload.user_id, product_id=payload.product_id
    ).first()
    if wishlist_item:
        db.delete(wishlist_item)
        db.commit()
        return {"message": "Removed from wishlist"}
    raise HTTPException(status_code=404, detail="Item not found in wishlist")
