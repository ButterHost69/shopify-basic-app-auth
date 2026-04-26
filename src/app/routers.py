from fastapi import FastAPI

from modules.V1.all_routers_V1 import router as v1_routers

def register_routers(app:FastAPI):
    app.include_router(v1_routers, tags=["V1"])