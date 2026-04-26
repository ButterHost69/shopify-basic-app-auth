from fastapi import APIRouter

from .ShopifyManager.routers import router as shopify_router


router = APIRouter()
router.include_router(shopify_router, tags=["Shopify Routers"])