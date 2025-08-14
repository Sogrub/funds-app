import time
from datetime import datetime
from typing import List, Optional
from app.core.notification import NotificationService
from app.modules.funds.repository import FundsRepository
from app.modules.subscriptions.models import SubscriptionModel, SubscriptionTypeEnum
from app.core.models.general_models import GenericResponse
from app.modules.subscriptions.models import SubscriptionResponseDto
from app.modules.subscriptions.repository import SubscriptionRepository
from app.modules.transactions.repository import TransactionRepository
from app.modules.users.repository import UserRepository


class SubscriptionService:
    def __init__(self) -> GenericResponse:
        self.users_repository = UserRepository()
        self.funds_repository = FundsRepository()
        self.transactions_repository = TransactionRepository()
        self.repository = SubscriptionRepository()
        self.notification = NotificationService()

    def list_subscriptions(self, user_id: int, fund_id: int):
        response = self.repository.list(user_id, fund_id)
        data = response.get("Items", [])
        subscriptions: List[SubscriptionResponseDto] = [SubscriptionResponseDto(**item) for item in data]
        safe_subscriptions = [subscription.model_dump(exclude={"password"}) for subscription in subscriptions]
        return GenericResponse[List[SubscriptionResponseDto]](message="Subscriptions retrieved successfully", status="success", data=safe_subscriptions)

    def create_subscription(self, subscription: SubscriptionModel) -> GenericResponse:
        user = self.users_repository.find_by_id(subscription.user_id)
        if not user:
            return GenericResponse[None](message="User not found", status="error", data=None)

        fund = self.funds_repository.find_by_id(subscription.fund_id)
        if not fund:
            return GenericResponse[None](message="Fund not found", status="error", data=None)
            
        if self.repository.find_by_user_id_and_fund_id(subscription.user_id, subscription.fund_id):
            return GenericResponse[None](message="Subscription already exists", status="error", data=None)

        balance = subscription.amount or 0
        user_balance = user.balance or 0
        if balance > user_balance:
            return GenericResponse[None](message="Insufficient funds", status="error", data=None)

        fund_minimum = fund.min_amount or 0
        if balance < fund_minimum:
            return GenericResponse[None](message="There are no available funds to link to fund {fund['name']}.", status="error", data=None)

        subscription_item = subscription.model_dump()
        subscription_item["id"] = int(time.time() * 1000)
        subscription_item["subscription_date"] = datetime.now().isoformat()
        subscription_item["type"] = "ACTIVE"

        subscription_created = self.repository.save(subscription_item)
        if subscription_created is None:
            return GenericResponse[None](message="Subscription creation failed", status="error", data=None)

        new_balance = user_balance - fund_minimum
        self.users_repository.update_balance(subscription.user_id, new_balance)

        self.transactions_repository.save(subscription.user_id, subscription.fund_id, "ACTIVE", subscription.amount)

        self.notification.send_email(user.email, "New subscription", f"You have successfully subscribed to {fund.name} with a balance of {balance}.")
        # self.notification.send_sms(user.phone_number, "You have successfully subscribed to {fund.name} with a balance of {balance}.")

        return GenericResponse[SubscriptionResponseDto](message="Subscription created successfully", status="success", data=subscription_created)

    def update_subscription(self, subscription_id: int, type: SubscriptionTypeEnum, amount: Optional[int] = None) -> GenericResponse:
        subscription = self.repository.find_by_id(subscription_id)
        if not subscription:
            return GenericResponse[None](message="Subscription not found", status="error", data=None)
        
        if subscription.type == type:
            return GenericResponse[None](message="Subscription already in this state", status="error", data=None)
        
        subscription_item = subscription.model_dump()
        new_amount = amount or subscription.amount
        if type == "ACTIVE":
            subscription_item["type"] = "ACTIVE"
            subscription_item["subscription_date"] = datetime.now().isoformat()
            subscription_item["cancellation_date"] = None
            subscription_item["amount"] = new_amount
        elif type == "CANCELLED":
            subscription_item["type"] = "CANCELLED"
            subscription_item["cancellation_date"] = datetime.now().isoformat()

        updated_subscription = self.repository.update(subscription_item)
        if updated_subscription is None:
            return GenericResponse[None](message="Subscription update failed", status="error", data=None)

        user = self.users_repository.find_by_id(subscription.user_id)
        if type == "CANCELLED":
            user_balance = user.balance or 0
            new_balance = user_balance + new_amount
            self.users_repository.update_balance(subscription.user_id, new_balance)
        else:
            user_balance = user.balance or 0
            new_balance = user_balance - new_amount
            self.users_repository.update_balance(subscription.user_id, new_balance)

        self.transactions_repository.save(subscription.user_id, subscription.fund_id, type, new_amount)

        return GenericResponse[SubscriptionResponseDto](message="Subscription updated successfully", status="success", data=updated_subscription)