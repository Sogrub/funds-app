from app.core.db import get_dynamodb_resource
from app.modules.users.models import UserModel


TABLE_NAME = "users"

class UserRepository:
    def __init__(self):
        self.dynamodb = get_dynamodb_resource()
        self.table = self.dynamodb.Table(TABLE_NAME)

    def list(self):
        response = self.table.scan()
        return response

    def create(self, user: UserModel):
        response = self.table.put_item(Item=user.dict())
        return response