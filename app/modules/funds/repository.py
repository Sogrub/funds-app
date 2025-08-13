import time
from app.modules.funds.models import FundModel, FundResponseDto
from app.core.db import get_dynamodb_resource
from boto3.dynamodb.conditions import Attr


TABLE_NAME = "funds"

class FundsRepository:
    def __init__(self):
        self.dynamodb = get_dynamodb_resource()
        self.table = self.dynamodb.Table(TABLE_NAME)

    def find_by_name(self, name: str):
        response = self.table.scan(
            FilterExpression=Attr("name").eq(name)
        )
        return response.get("Items", [])

    def save(self, fund: FundModel) -> FundResponseDto | None:
        item = fund.model_dump()
        item["id"] = int(time.time() * 1000)
        response = self.table.put_item(Item=item)
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            safe_fund_data = {k: v for k, v in item.items() if k != "password"}
            return FundResponseDto(**safe_fund_data)
        else:
            return None

    def list(self):
        response = self.table.scan()
        return response

    def find_by_id(self, id: int) -> FundResponseDto | None:
        response = self.table.get_item(
            Key={"id": id}
            )
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            return FundResponseDto(**response.get("Item", {}))
        else:
            return None
