from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date
from enum import Enum

class DiscountType(str, Enum):
    percentage = "percentage"
    fixed = "fixed"

class PromoStatus(str, Enum):
    active = "active"
    non_active = "non_active"

class PromoBase(BaseModel):
    name: str
    description: Optional[str] = ""
    discount_type: DiscountType
    discount_value: int = Field(..., gt=0)
    expiry_date: date
    status: Optional[PromoStatus] = PromoStatus.active

    @validator("expiry_date")
    def validate_future_date(cls, v):
        if v <= date.today():
            raise ValueError("Expiry date must be in the future")
        return v

    @validator("discount_value")
    def validate_discount_value(cls, v, values):
        if values.get("discount_type") == "percentage" and not (1 <= v <= 100):
            raise ValueError("Percentage discount must be between 1 and 100")
        return v

class PromoCreate(PromoBase):
    pass

class PromoUpdate(PromoBase):
    pass

class PromoResponse(PromoBase):
    id: int

    class Config:
        from_attributes = True
