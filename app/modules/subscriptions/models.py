from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class SubscriptionTypeEnum(str, Enum):
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"

class SubscriptionModel(BaseModel):
    user_id: int
    fund_id: int
    amount: int

class SubscriptionResponseDto(BaseModel):
    id: int
    user_id: int
    fund_id: int
    amount: int
    type: SubscriptionTypeEnum
    subscription_date: Optional[str] = None
    cancellation_date: Optional[str] = None
