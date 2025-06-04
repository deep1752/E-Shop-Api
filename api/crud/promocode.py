from sqlalchemy.orm import Session
from api.database.models.promocode import PromoCode
from api.database.schemas.promocode import PromoCreate, PromoUpdate

def get_all_promos(db: Session, promo_id: int = None):
    if promo_id:
        return db.query(PromoCode).filter(PromoCode.id == promo_id).first()
    return db.query(PromoCode).all()

def create_promo(db: Session, promo: PromoCreate):
    db_promo = PromoCode(**promo.dict())
    db.add(db_promo)
    db.commit()
    db.refresh(db_promo)
    return db_promo

def update_promo(db: Session, promo_id: int, promo: PromoUpdate):
    db_promo = db.query(PromoCode).filter(PromoCode.id == promo_id).first()
    if db_promo:
        for key, value in promo.dict().items():
            setattr(db_promo, key, value)
        db.commit()
        db.refresh(db_promo)
    return db_promo

def delete_promo(db: Session, promo_id: int):
    db_promo = db.query(PromoCode).filter(PromoCode.id == promo_id).first()
    if db_promo:
        db.delete(db_promo)
        db.commit()
        return True
    return False
