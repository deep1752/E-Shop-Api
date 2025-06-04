from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.database.schemas.products import (
    ProductsCreate, ProductsUpdate, ProductsResponse, ProductWithCategory
)
from api.crud.product import (
    create_product, delete_product, get_all_products, get_product_by_id,
    update_product, bulk_add_products, get_product_by_ids
)
from typing import List




# Initialize a router instance for product-related routes
router = APIRouter()


# ----------------------------------------------------------------------------
# Route: POST /add
# Description: Bulk add multiple products at once
# ----------------------------------------------------------------------------
@router.post("/add", response_model=List[ProductsResponse])
def add(product: List[ProductsCreate], db: Session = Depends(get_db)):
    """
    Add multiple products to the database in one API call.

    Parameters:
    - product: List of product objects to be added.
    - db: Database session.

    Returns:
    - A list of the newly created products.
    """
    return bulk_add_products(db, product)


# ----------------------------------------------------------------------------
# Route: GET /all_products
# Description: Fetch all products, optionally filtered by category
# ----------------------------------------------------------------------------
@router.get("/all_products", response_model=List[ProductWithCategory])
def list_products(category: str = None, db: Session = Depends(get_db)):
    """
    Retrieve all products, with optional category filter.

    Parameters:
    - category: Optional category name to filter products.
    - db: Database session.

    Returns:
    - List of all products (with category data) or filtered products.
    """
    return get_all_products(db, category)


# ----------------------------------------------------------------------------
# Route: GET /get_product/{slug}
# Description: Retrieve a product by its slug (usually URL-friendly name)
# ----------------------------------------------------------------------------
@router.get("/get_product/{slug}", response_model=ProductsResponse)
def get_single_product(slug: str, db: Session = Depends(get_db)):
    """
    Retrieve a single product by its unique slug.

    Parameters:
    - slug: Slug value of the product.
    - db: Database session.

    Returns:
    - The product data if found.
    """
    return get_product_by_id(db, slug)


# ----------------------------------------------------------------------------
# Route: DELETE /delete/{product_id}
# Description: Delete a product by its unique ID
# ----------------------------------------------------------------------------
@router.delete("/delete/{product_id}", response_model=dict)
def delete(product_id: int, db: Session = Depends(get_db)):
    """
    Delete a product by its ID.

    Parameters:
    - product_id: Unique identifier of the product.
    - db: Database session.

    Returns:
    - A success message or error if not found.
    """
    return delete_product(db, product_id)


# ----------------------------------------------------------------------------
# Route: PUT /product_update/{product_id}
# Description: Update a product’s details by ID
# ----------------------------------------------------------------------------
@router.put("/product_update/{product_id}", response_model=ProductsResponse)
def update_product_api(product_id: int, product: ProductsUpdate, db: Session = Depends(get_db)):
    """
    Update an existing product by its ID.

    Parameters:
    - product_id: ID of the product to update.
    - product: ProductUpdate schema with new data.
    - db: Database session.

    Returns:
    - The updated product or error if not found.
    """
    updated_product = update_product(db, product_id, product)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


# ----------------------------------------------------------------------------
# Route: GET /by-id/{product_id}
# Description: Get product details by ID (alternative to slug-based fetch)
# ----------------------------------------------------------------------------
@router.get("/by-id/{product_id}", response_model=ProductsResponse)
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a product by its numeric ID.

    Parameters:
    - product_id: Unique identifier of the product.
    - db: Database session.

    Returns:
    - The product data or 404 error if not found.
    """
    product = get_product_by_ids(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product