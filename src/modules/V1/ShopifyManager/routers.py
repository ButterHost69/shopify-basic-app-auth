from fastapi import APIRouter, Request
from .controller import handle_auth, handle_products

router = APIRouter(prefix="/shopify")



@router.get("/auth/{shop_name}")
async def auth_app(req: Request, shop_name:str):
    return await handle_auth(req.method, req, shop_name)
    

# This is purely for acting as a redirect.
@router.get("/done")
async def verify_auth(req: Request):
    return await handle_auth(req.method, req)


@router.get("/{shop_name}/get-products")
async def get_products(req: Request, shop_name:str):
    return await handle_products(req.method, req, shop_name)
