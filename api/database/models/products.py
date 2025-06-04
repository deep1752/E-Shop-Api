from sqlalchemy import Column, Integer, Float, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from api.database.connection import Base

class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=True)
    description = Column(String(100), nullable=False)
    mrp = Column(Float)
    net_price = Column(Float)
    quantity_in_stock = Column(Integer)
    image = Column(String(255), nullable=False)
    product_cat = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, nullable=True)

    # Relationship to Categories
    category = relationship("Categories", backref="products")
