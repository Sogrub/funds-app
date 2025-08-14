from typing import Optional
from fastapi import APIRouter, Query
from app.modules.subscriptions.models import SubscriptionModel, SubscriptionTypeEnum
from app.modules.subscriptions.services import SubscriptionService


router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

subscriptionService = SubscriptionService()

@router.get("/")
def list_subscriptions(
    user_id: Optional[int] = Query(None),
    fund_id: Optional[int] = Query(None)
):
    return subscriptionService.list_subscriptions(user_id, fund_id)

@router.post("/")
def create_subscription(subscription: SubscriptionModel):
    return subscriptionService.create_subscription(subscription)

@router.patch("/{subscription_id}")
def update_subscription(subscription_id: int, type: SubscriptionTypeEnum, amount: Optional[int] = None):
    return subscriptionService.update_subscription(subscription_id, type, amount)