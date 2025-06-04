from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum
import datetime
from api.database.connection import Base


class DiscountType(str, enum.Enum):
    percentage = "percentage"
    fixed = "fixed"

class PromoStatus(str, enum.Enum):
    active = "active"
    non_active = "non_active"

class PromoCode(Base):
    __tablename__ = "promocodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    discount_type = Column(Enum(DiscountType), nullable=False)
    discount_value = Column(Integer, nullable=False)
    expiry_date = Column(Date, nullable=False)
    status = Column(Enum(PromoStatus), default=PromoStatus.active)
