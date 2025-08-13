from fastapi import APIRouter
from app.modules.users.models import UserModel
from app.modules.users.services import UserService

router = APIRouter(prefix="/users", tags=["Users"])

userService = UserService()

@router.get("/")
def list_users():
    return userService.list_users()

@router.post("/")
def create_user(user: UserModel):
    return userService.create_user(user)

@router.put("/{id}/balance")
def update_balance(id: int, balance: int):
    return userService.update_balance(id, balance)