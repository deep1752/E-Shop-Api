from sqlalchemy.orm import Session
from api.database.models.categories import Categories
from api.database.models.products   import Products  
from api.database.schemas.categories import CategoryCreate,categoryUpdate
from datetime import datetime
from fastapi import HTTPException


def create_category(db: Session, category: CategoryCreate):
    created_at = category.created_at or datetime.utcnow()

    db_category = Categories(
        name=category.name,
        created_at=datetime.utcnow(),
        updated_at=None
       
    )
    db.add(db_category)  # Add the user to the database session
    db.commit()  # Commit the transaction to save changes
    db.refresh(db_category)  # Refresh the user instance with the latest data from DB
    return db_category

# okk

def delete_category(db: Session, category_id: int):
    category = db.query(Categories).filter(Categories.id == category_id).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Check if any products are linked to this category
    linked_products = db.query(Products).filter(Products.category_id == category_id).all()

    if linked_products:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category: it is linked to one or more products"
        )

    db.delete(category)
    db.commit()
    return {"success": True, "message": "Category deleted successfully"}

def get_all_category(db: Session):
    """
    Fetches all category from the database.
    
    :param db: Database session.
    :return: A list of all category.
    """
    return db.query(Categories).all()




def update_category(db: Session, category_id: int, category_data: categoryUpdate):
    category = db.query(Categories).filter(Categories.id == category_id).first()
    if not category:
        return None

    for key, value in category_data.dict(exclude_unset=True).items():
        setattr(category, key, value)

    category.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(category)
    return category



def get_category_by_id(db: Session, category_id: int):
    """
    Fetch a category by its ID.
    """
    return db.query(Categories).filter(Categories.id == category_id).first()
