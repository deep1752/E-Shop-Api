from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from api.database.connection import Base

class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
