from sqlalchemy import select, update, or_

from .schemas import ShopifyClientDataBase
from .models import ShopifyClientData
from app.database import fetch_all, fetch_one, create, delete_all
from app.database import DBAsyncSession


class ShopifyClientDataDAO:
    @staticmethod
    async def get_clientData_by_shop_name(shop_name: str):
        query = select(ShopifyClientData).where(ShopifyClientData.shop_name == shop_name)
        return await fetch_one(query=query)

    @staticmethod
    async def get_all_clientData():
        query = select(ShopifyClientData)
        return await fetch_all(query=query)

    @staticmethod
    async def save_clientData(data: ShopifyClientDataBase):
        data = ShopifyClientData(**data.model_dump())
        return await create(data)
