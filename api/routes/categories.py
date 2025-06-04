from fastapi import APIRouter, Depends,HTTPException, Query
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.database.schemas.categories import CategoryCreate, CategoryResponse,categoryUpdate
from api.crud.category import create_category,delete_category,get_all_category,update_category,get_category_by_id
from typing import List, Optional, Union


# Create a new API router for handling authentication-related endpoints
router = APIRouter()


@router.post("/add" , response_model=CategoryResponse)
def add(category: CategoryCreate, db: Session = Depends(get_db)):
 
    return create_category(db,category)


@router.delete("/delete/{category_id}", response_model=dict)
def delete(category_id: int, db: Session = Depends(get_db)):
    return delete_category(db, category_id)



# @router.get("/all_category", response_model=List[CategoryResponse])
# def list_category(db: Session = Depends(get_db)):
#     return get_all_category(db)


@router.get("/categories", response_model=Union[CategoryResponse, List[CategoryResponse]])
def get_categories(category_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    if category_id is not None:
        category = get_category_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    return get_all_category(db)


@router.put("/category_update/{category_id}", response_model=CategoryResponse)
def update_category_api(category_id: int, category: categoryUpdate, db: Session = Depends(get_db)):
    updated_category = update_category(db, category_id, category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="category not found")
    return updated_category

