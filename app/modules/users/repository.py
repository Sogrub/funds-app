import time
from app.core.db import get_dynamodb_resource
from app.modules.users.models import UserModel, UserResponseDto
from boto3.dynamodb.conditions import Attr


TABLE_NAME = "users"

class UserRepository:
    def __init__(self):
        self.dynamodb = get_dynamodb_resource()
        self.table = self.dynamodb.Table(TABLE_NAME)

    def list(self):
        response = self.table.scan()
        return response

    def save(self, user: UserModel) -> UserResponseDto | None:
        item = user.model_dump()
        item["id"] = int(time.time() * 1000)
        item["balance"] = 500000
        print(item)
        response = self.table.put_item(Item=item)
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            safe_user_data = {k: v for k, v in item.items() if k != "password"}
            return UserResponseDto(**safe_user_data)
        else:
            return None

    def find_by_email(self, email: str):
        response = self.table.scan(
            FilterExpression=Attr("email").eq(email)
        )
        return response.get("Items", [])

    def find_by_id(self, id: int) -> UserResponseDto | None:
        response = self.table.get_item(
            Key={"id": id}
            )
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            return UserResponseDto(**response.get("Item", {}))
        else:
            return None

    # Return modified User
    def update_balance(self, id: int, balance: int) -> UserResponseDto | None:
        response = self.table.update_item(
            Key={"id": id},
            UpdateExpression="set balance = :balance",
            ExpressionAttributeValues={":balance": balance},
            ReturnValues="ALL_NEW"
        )
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            return UserResponseDto(**response.get("Attributes", {}))
        else:
            return None