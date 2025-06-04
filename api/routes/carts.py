from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.database.schemas.carts import CartsCreate, CartsResponse
from api.crud.carts import create_cart,delete_cart,get_carts
from typing import List, Optional


# Create a new API router for handling authentication-related endpoints
router = APIRouter()


@router.post("/add" , response_model=CartsResponse)
def add(cart: CartsCreate, db: Session = Depends(get_db)):
 
    return create_cart(db,cart)


@router.delete("/delete/{cart_id}", response_model=dict)
def delete(cart_id: int, db: Session = Depends(get_db)):
    return delete_cart(db, cart_id)


@router.get("/", response_model=List[CartsResponse])
def list_carts(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """
    Endpoint to get carts.
    - If `user_id` is provided as a query param, filters carts for that user.
    - If not provided, returns all carts.
    Example:
    - /carts/ → all carts
    - /carts/?user_id=1 → carts for user with ID 1
    """
    return get_carts(db, user_id)