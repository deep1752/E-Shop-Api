from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CategoryCreate(BaseModel):
    name: str
    created_at:datetime
    updated_at: Optional[datetime] = None

class categoryUpdate(BaseModel):
    name: str
   
class CategoryResponse(BaseModel):
    id: int
    name: str
    created_at:datetime
    updated_at:Optional[datetime]



    class Config:
        from_attributes = True

