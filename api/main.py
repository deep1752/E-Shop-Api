from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Log startup to Vercel logs
print("🚀 FastAPI app starting on Vercel...")

# ----------------------------------------------------------------------------
# FASTAPI APPLICATION INITIALIZATION
# ----------------------------------------------------------------------------
app = FastAPI()

# ----------------------------------------------------------------------------
# CORS MIDDLEWARE SETUP
# ----------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------------
# DATABASE INITIALIZATION
# ----------------------------------------------------------------------------
try:
    from api.database.connection import engine
    from api.database.base import Base

    # Ensure tables are created
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables initialized.")
except Exception as db_error:
    print("❌ Database Initialization Error:", db_error)

# ----------------------------------------------------------------------------
# ROUTES IMPORT
# ----------------------------------------------------------------------------
try:
    from api.routes import (
        auth, users, categories, products, address,
        carts, reviews, orders, product_img, promocode,
        wishlist, contact
    )

    # Auth Routes (Register, Login)
    app.include_router(auth.router, prefix="/auth", tags=["Auth"])

    # User Routes
    app.include_router(users.router, prefix="/users", tags=["Users"])

    # Category Routes
    app.include_router(categories.router, prefix="/categories", tags=["Categories"])

    # Product Routes
    app.include_router(products.router, prefix="/products", tags=["Products"])

    # Address Routes
    app.include_router(address.router, prefix="/address", tags=["Address"])

    # Cart Routes
    app.include_router(carts.router, prefix="/cart", tags=["Cart"])

    # Review Routes
    app.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])

    # Order Routes
    app.include_router(orders.router, prefix="/orders", tags=["Orders"])

    # Product Image Routes
    app.include_router(product_img.router, prefix="/product_img", tags=["Product_img"])

    # Promo Code Routes
    app.include_router(promocode.router, prefix="/promocode", tags=["Promocode"])

    # Wishlist Routes
    app.include_router(wishlist.router, prefix="/wishlist", tags=["Wishlist"])

    # Contact Routes
    app.include_router(contact.router, prefix="/contact", tags=["Contact"])

    print("✅ Routers loaded successfully.")

except Exception as route_error:
    print("❌ Router Import Error:", route_error)

# ----------------------------------------------------------------------------
# ROOT ENDPOINT
# ----------------------------------------------------------------------------
@app.get("/")
def read_root():
    return {"message": "✅ FastAPI main.py is working on Vercel"}
