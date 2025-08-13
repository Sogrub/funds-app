from pydantic import BaseModel

from app.modules.subscriptions.models import SubscriptionTypeEnum

class TransactionModel(BaseModel):
    id: int
    user_id: int
    fund_id: int
    type: SubscriptionTypeEnum
    amount: int
    date: str