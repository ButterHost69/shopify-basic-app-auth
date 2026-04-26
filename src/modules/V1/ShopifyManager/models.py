# app/models/contact.py
from sqlalchemy import Boolean, Column, String, Integer, DateTime
from sqlalchemy.sql import func
from app.database import DB_Base 

class ShopifyClientData(DB_Base):
    __tablename__ = "shopifyClientData"

    id              = Column(Integer, primary_key=True, index=True)
    shop_name       = Column(String(255), nullable=True)
    access_token    = Column(String(255), nullable=True)   
    scope           = Column(String(255), nullable=True)   
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now()
    )
