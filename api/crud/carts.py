from sqlalchemy.orm import Session
from api.database.models.carts import Carts
from api.database.schemas.carts import CartsCreate
from datetime import datetime


def create_cart(db: Session, cart: CartsCreate):
    created_at = cart.created_at or datetime.utcnow()

    db_cart = Carts(
        user_id=cart.user_id,
        product_id=cart.product_id,
        quantity=cart.quantity,
        created_at=cart.created_at,
       
    )
    db.add(db_cart)  # Add the user to the database session
    db.commit()  # Commit the transaction to save changes
    db.refresh(db_cart)  # Refresh the user instance with the latest data from DB
    return db_cart

# okk

def delete_cart(db: Session, cart_id: int):
     
    cart = db.query(Carts).filter(Carts.id == cart_id).first()
    if cart:
        db.delete(cart)
        db.commit()
        return {"success": True,"message": "cart deleted successfully"}
    
    return {"success": False,"message": "cart not found"}

def get_carts(db: Session, user_id: int = None):
    """
    Gets all carts or filters them by user_id if provided.

    :param db: Database session.
    :param user_id: Optional user ID to filter carts.
    :return: List of carts.
    """
    if user_id:
        return db.query(Carts).filter(Carts.user_id == user_id).all()
    return db.query(Carts).all()