
from datetime import datetime
import time
from typing import List, Optional
from app.core.models.general_models import GenericResponse
from app.core.db import get_dynamodb_resource
from app.modules.subscriptions.models import SubscriptionTypeEnum
from app.modules.transactions.models import TransactionModel


TABLE_NAME = "transactions"

class TransactionRepository:
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

    def save(self, user_id: int, fund_id: int, type: SubscriptionTypeEnum, amount: int):
        transaction = TransactionModel(id=int(time.time() * 1000), user_id=user_id, fund_id=fund_id, type=type, amount=amount, date=datetime.now().isoformat())
        self.table.put_item(Item=transaction.model_dump())
        
        