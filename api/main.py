from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import auth, users, categories, products, address, carts, reviews, orders,product_img , promocode, wishlist, contact
from api.database.connection import engine
from api.database.base import Base

# ----------------------------------------------------------------------------
# DATABASE INITIALIZATION
# ----------------------------------------------------------------------------
# Automatically create tables in the database if they do not exist
Base.metadata.create_all(bind=engine)


# ----------------------------------------------------------------------------
# FASTAPI APPLICATION INITIALIZATION
# ----------------------------------------------------------------------------
# Create the FastAPI app instance
app = FastAPI()


# ----------------------------------------------------------------------------
# MIDDLEWARE SETUP
# ----------------------------------------------------------------------------
# Enable CORS (Cross-Origin Resource Sharing) to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Accept requests from any origin (you can restrict to ["http://localhost:3000"] for dev)
    allow_credentials=True,        # Allow sending cookies/headers
    allow_methods=["*"],           # Accept all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],           # Accept all HTTP headers
)


# ----------------------------------------------------------------------------
# ROUTE INCLUSION - Modular API Structure
# ----------------------------------------------------------------------------

# Auth Routes (Register, Login)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# User Routes (User CRUD operations)
app.include_router(users.router, prefix="/users", tags=["Users"])

# Category Routes (Add/Edit/Delete/Get categories)
app.include_router(categories.router, prefix="/categories", tags=["Categories"])

# Product Routes (CRUD for products)
app.include_router(products.router, prefix="/products", tags=["Products"])

# Address Routes (User shipping addresses)
app.include_router(address.router, prefix="/address", tags=["Address"])

# Cart Routes (Add/remove/view cart items)
app.include_router(carts.router, prefix="/cart", tags=["Cart"])

# Review Routes (Add/view product reviews)
app.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])

# Order Routes (Create orders, get order history)
app.include_router(orders.router, prefix="/orders", tags=["Orders"])

# Product Image Upload Routes (Manage product images)
app.include_router(product_img.router, prefix="/product_img", tags=["Product_img"])

# Promo Code Routes (Create/apply promo codes)
app.include_router(promocode.router, prefix="/promocode", tags=["Promocode"])

# Wishlist Routes (Add/remove items from wishlist)
app.include_router(wishlist.router, prefix="/wishlist", tags=["Wishlist"])

# Contact/Support Routes (Submit inquiries, messages)
app.include_router(contact.router, prefix="/contact", tags=["Contact"])


# ----------------------------------------------------------------------------
# END OF MAIN APPLICATION
# ----------------------------------------------------------------------------