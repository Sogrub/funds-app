from fastapi import APIRouter
from app.api.v1.routers.users import router as users_router

api_router = APIRouter()
api_router.include_router(users_router)