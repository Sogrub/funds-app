from typing import Dict, Optional
from app.modules.subscriptions.models import SubscriptionModel, SubscriptionResponseDto
from app.core.db import get_dynamodb_resource
from boto3.dynamodb.conditions import Attr
import time

TABLE_NAME = "subscriptions"

class SubscriptionRepository:
    def __init__(self):
        self.dynamodb = get_dynamodb_resource()
        self.table = self.dynamodb.Table(TABLE_NAME)

    def list(self, user_id: Optional[int] = None, fund_id: Optional[int] = None):
        filter_expression = None
        expression_attribute_values = {}

        if user_id is not None:
            filter_expression = "user_id = :user_id"
            expression_attribute_values[":user_id"] = user_id

        if fund_id is not None:
            if filter_expression:
                filter_expression += " AND fund_id = :fund_id"
            else:
                filter_expression = "fund_id = :fund_id"
            expression_attribute_values[":fund_id"] = fund_id

        if filter_expression:
            response = self.table.scan(
                FilterExpression=filter_expression,
                ExpressionAttributeValues=expression_attribute_values
            )
        else:
            response = self.table.scan()

        return response

    def find_by_id(self, id: int) -> SubscriptionResponseDto | None:
        response = self.table.get_item(Key={"id": id})
    
        item = response.get("Item")
        if not item:
            return None
        
        return SubscriptionResponseDto(**item)

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
                "#type = :type, "
                "#amount = :amount"
            ),
            ExpressionAttributeNames={
                "#type": "type",
                "#amount": "amount"
            },
            ExpressionAttributeValues={
                ":subscription_date": subscription["subscription_date"],
                ":cancellation_date": subscription["cancellation_date"],
                ":type": subscription["type"],
                ":amount": subscription["amount"]
            },
            ReturnValues="ALL_NEW"
        )

        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            return SubscriptionResponseDto(**response.get("Attributes", {}))
        else:
            return None
