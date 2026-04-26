import secrets

from fastapi import FastAPI, Request

from .settings import import_settings
from .utility import exception_handler
from .project_schema import ApiResponse
from .routers import register_routers
from .database import init_db

from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.middleware.sessions import SessionMiddleware
    
from contextlib import asynccontextmanager


settings = import_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("!! Starting Server !!")
    await init_db()
    yield
    print("!! Closing Server !!")

app = FastAPI(
    title=settings.app_settings.project_name,
    version=settings.app_settings.api_version,
    lifespan=lifespan
)

app.add_middleware(
    SessionMiddleware,
    secret_key=secrets.token_urlsafe(32)
)

@app.exception_handler(Exception)
async def global_exception_handler(request:Request, e:Exception):
    tb = exception_handler(e, request)
    response = ApiResponse.error(message="Internal Server Error", code=HTTP_500_INTERNAL_SERVER_ERROR)
    response.data = {"traceback": tb}
    return response


@app.get("/", tags=["root"])
async def root() -> dict[str,str]:
    return {
        "message":"Hello World"
    }

register_routers(app)