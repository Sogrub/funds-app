from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routers import api_router
from app.core.config import get_settings
from app.core.db import init_dynamodb_table
from app.core.logger import logger

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🚀 Startup
    logger.info("App is starting...")
    if settings.app_env == "development":
        init_dynamodb_table("users")
        init_dynamodb_table("funds")
        init_dynamodb_table("subscriptions")
        init_dynamodb_table("transactions")
    yield
    # 🛑 Shutdown
    logger.info("App is shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        docs_url=settings.app_docs_url,
        redoc_url=settings.app_redoc_url,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    return app


app = create_app()
