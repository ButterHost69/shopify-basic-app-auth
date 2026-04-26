from datetime import datetime, timedelta
import secrets
import urllib

import requests

from .dao import ShopifyClientDataDAO 
from .schemas import ShopifyClientDataBase 


class ShopifyClientDataService:
    @staticmethod
    async def get_token(shop_name:str):
        client_data = await ShopifyClientDataDAO.get_clientData_by_shop_name(shop_name)
        if client_data:
            return ShopifyClientDataBase.model_validate(client_data[0]).access_token 
        return ""

    @staticmethod
    async def save(data):
        client_data = ShopifyClientDataBase(**data)
        id_ = await ShopifyClientDataDAO.save_clientData(client_data)
        return {"id": id_}, 200


class ShopifyService:
    @staticmethod
    def get_products(shop_name: str, access_token: str):
        resp = requests.get(
            f"https://{shop_name}.com/admin/api/2026-04/products.json",
            headers={"X-Shopify-Access-Token": access_token},
        )
        resp.raise_for_status()
        return resp.json(), resp.status_code

    @staticmethod
    def build_auth_url(shop_name:str, client_id:str, scope:str, redirect_url:str):
        state = secrets.token_urlsafe(32)
        
        params = {
            "client_id": client_id,
            "scope": scope,
            "redirect_uri": redirect_url,
            "state": state,
        }
        # if access_mode == "online":
        #     params["grant_options[]"] = "per-user"
        url = f"https://{shop_name}.com/admin/oauth/authorize?{urllib.parse.urlencode(params)}" # type: ignore
        return url, state

    @staticmethod
    def exchange_code_for_token(shop_name: str, client_id: str, client_secret: str, code: str):
        resp = requests.post(
            f"https://{shop_name}/admin/oauth/access_token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                # "expiring": "1",    # uncomment for an expiring offline token
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
        )
        resp.raise_for_status()
        return resp.json()