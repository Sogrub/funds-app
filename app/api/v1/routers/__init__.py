from fastapi import APIRouter
from app.api.v1.routers.users import router as users_router
from app.api.v1.routers.funds import router as funds_router
from app.api.v1.routers.subscriptions import router as subscriptions_router
from app.api.v1.routers.transactions import router as transactions_router

api_router = APIRouter()
api_router.include_router(users_router)
api_router.include_router(funds_router)
api_router.include_router(subscriptions_router)
api_router.include_router(transactions_router)