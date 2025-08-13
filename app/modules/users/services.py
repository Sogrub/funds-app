from typing import List
from app.core.models.general_models import GenericResponse
from app.modules.users.models import UserModel, UserResponseDto
from app.modules.users.repository import UserRepository


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def list_users(self) -> GenericResponse:
        response = self.repository.list()
        data = response.get("Items", [])

        users: List[UserResponseDto] = [UserResponseDto(**item) for item in data]
        safe_users = [user.model_dump(exclude={"password"}) for user in users]
        return GenericResponse[List[UserResponseDto]](message="Users retrieved successfully", status="success", data=safe_users)

    def create_user(self, user: UserModel) -> GenericResponse:
        if self.repository.find_by_email(user.email):
            return GenericResponse[None](message="User already exists", status="error", data=None)
        user_created = self.repository.save(user)
        if user_created is None:
            return GenericResponse[None](message="User creation failed", status="error", data=None)

        return GenericResponse[UserResponseDto](message="User created successfully", status="success", data=user_created)

    def update_balance(self, id: int, balance: int) -> GenericResponse:
        user = self.repository.find_by_id(id)
        if not user:
            return GenericResponse[None](message="User not found", status="error", data=None)
        user_updated = self.repository.update_balance(id, balance)
        if user_updated is None:
            return GenericResponse[None](message="User balance update failed", status="error", data=None)

        return GenericResponse[UserResponseDto](message="User balance updated successfully", status="success", data=user_updated)
