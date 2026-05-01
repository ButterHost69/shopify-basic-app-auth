import secrets
from typing import Optional
import urllib
import requests

from fastapi import Request
from app.main import ApiResponse
from fastapi.responses import RedirectResponse
from app.settings import import_settings
from app.utility import verify_hmac


from .services import ShopifyClientDataService, ShopifyService

async def handle_list_stores(request_type: str, req: Request):
    match request_type:
        case "GET":
            result, status_code = await ShopifyClientDataService.get_all()
            return ApiResponse.success(data=result, message="All stored tokens", code=status_code)
        case _:
            return ApiResponse.error(message="Method not allowed", code=405, data=None)

async def handle_auth(request_type: str, req: Request, shop_name:Optional[str]=None):
    config = import_settings()
    match request_type:
        case "GET":
            if shop_name:
                config = import_settings()
                url, state = ShopifyService.build_auth_url(
                    shop_name=shop_name, 
                    client_id = config.shopify_settings.shopify_app_cliend_id,
                    redirect_url= config.shopify_settings.shopify_app_redirect_url,
                    scope=config.shopify_settings.shopify_app_scopes,
                )
                req.session["state"] = state
                return RedirectResponse(url=url)
            
            else:
                stored_state = req.session.pop("state")
                if req.query_params.get("state") != stored_state:
                    return ApiResponse.error(message="state mismatch", code=301, data=None)
                
                if not verify_hmac(dict(req.query_params), config.shopify_settings.shopify_app_secret):
                    return ApiResponse.error(message="HMAC verification failed", code=301, data=None)
                            
                shop = req.query_params.get("shop", "")
                code = req.query_params.get("code", "")
                token_data = ShopifyService.exchange_code_for_token(
                    shop, 
                    config.shopify_settings.shopify_app_cliend_id,
                    config.shopify_settings.shopify_app_secret,
                    code,
                )
                
                result, status_code = await ShopifyClientDataService.save({
                    "shop_name":shop,
                    "access_token":token_data["access_token"],
                    "scope":token_data["scope"]
                })
                message = f"Succesfully Connected Store: {shop} to the App"
                
        case _:
            return ApiResponse.error(message="Method not allowed", code=405, data=None)
                 
    return ApiResponse.success(data=result, message=message, code=status_code)      

async def handle_products(request_type: str, req: Request, shop_name:str):
    access_token = await ShopifyClientDataService.get_token(shop_name)
    if access_token:
        result, status_code = ShopifyService.get_products(shop_name, access_token)
        message = "fetched from shopify"
        return ApiResponse.success(data=result, message=message, code=status_code)      
    else:
        return ApiResponse.error(message=f"access token not found for shop:{shop_name}", code=405, data=None)