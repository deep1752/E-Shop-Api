from sqlalchemy import Column, Integer, Text,ForeignKey
from api.database.connection import Base

class ProductImage(Base):
    __tablename__ = "product_images"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    image = Column(Text, nullable=False)
