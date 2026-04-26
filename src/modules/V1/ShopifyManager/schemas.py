# app/schemas/contact_schema.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ShopifyClientDataBase(BaseModel):
    id:Optional[int] = None
    
    shop_name:Optional[str] = None
    access_token:Optional[str] = None
    scope:Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True