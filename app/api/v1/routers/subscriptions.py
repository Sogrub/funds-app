from fastapi import APIRouter
from app.modules.subscriptions.models import SubscriptionModel, SubscriptionTypeEnum
from app.modules.subscriptions.services import SubscriptionService


router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

subscriptionService = SubscriptionService()

@router.get("/")
def list_subscriptions():
    return subscriptionService.list_subscriptions()

@router.post("/")
def create_subscription(subscription: SubscriptionModel):
    return subscriptionService.create_subscription(subscription)

@router.patch("/{subscription_id}")
def update_subscription(subscription_id: int, type: SubscriptionTypeEnum):
    return subscriptionService.update_subscription(subscription_id, type)