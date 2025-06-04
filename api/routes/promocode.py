from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from api.database.connection import get_db
from api.database.schemas.promocode import PromoCreate, PromoResponse, PromoUpdate
import api.crud.promocode as crud

router = APIRouter()

@router.get("/", response_model=List[PromoResponse])
def read_promos(promo_id: int = Query(None), db: Session = Depends(get_db)):
    result = crud.get_all_promos(db, promo_id)
    if promo_id and not result:
        raise HTTPException(status_code=404, detail="Promo code not found")
    return [result] if promo_id else result

# ✅ UPDATED: Accept list of promo codes
@router.post("/add", response_model=List[PromoResponse])
def create_promos(promos: List[PromoCreate], db: Session = Depends(get_db)):
    created_promos = []
    for promo in promos:
        created = crud.create_promo(db, promo)
        created_promos.append(created)
    return created_promos

@router.put("/update/{promo_id}", response_model=PromoResponse)
def update_promo(promo_id: int, promo: PromoUpdate, db: Session = Depends(get_db)):
    updated = crud.update_promo(db, promo_id, promo)
    if not updated:
        raise HTTPException(status_code=404, detail="Promo code not found")
    return updated

@router.delete("/delete/{promo_id}")
def delete_promo(promo_id: int, db: Session = Depends(get_db)):
    success = crud.delete_promo(db, promo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Promo code not found")
    return {"success": True, "message": "Promo code deleted successfully"}
