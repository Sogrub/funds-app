from typing import Dict
from app.modules.subscriptions.models import SubscriptionModel, SubscriptionResponseDto
from app.core.db import get_dynamodb_resource
from boto3.dynamodb.conditions import Attr
import time

TABLE_NAME = "subscriptions"

class SubscriptionRepository:
    def __init__(self):
        self.dynamodb = get_dynamodb_resource()
        self.table = self.dynamodb.Table(TABLE_NAME)

    def list(self):
        response = self.table.scan()
        return response

    def find_by_id(self, id: int) -> SubscriptionResponseDto | None:
        response = self.table.get_item(
            Key={"id": id}
            )
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            return SubscriptionResponseDto(**response.get("Item", {}))
        else:
            return None

    def find_by_user_id_and_fund_id(self, user_id: int, fund_id: int):
        response = self.table.scan(
            FilterExpression=Attr("user_id").eq(user_id) & Attr("fund_id").eq(fund_id)
        )
        return response.get("Items", [])

    def save(self, subscription: Dict) -> SubscriptionResponseDto | None:
        self.table.put_item(Item=subscription)
        return subscription

    def update(self, subscription: Dict) -> SubscriptionResponseDto | None:
        response = self.table.update_item(
            Key={"id": subscription["id"]},
            UpdateExpression=(
                "set subscription_date = :subscription_date, "
                "cancellation_date = :cancellation_date, "
                "#type = :type"
            ),
            ExpressionAttributeNames={
                "#type": "type"
            },
            ExpressionAttributeValues={
                ":subscription_date": subscription["subscription_date"],
                ":cancellation_date": subscription["cancellation_date"],
                ":type": subscription["type"]
            },
            ReturnValues="ALL_NEW"
        )

        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            return SubscriptionResponseDto(**response.get("Attributes", {}))
        else:
            return None
