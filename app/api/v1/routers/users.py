from fastapi import APIRouter
from app.modules.users.models import UserModel
from app.modules.users.repository import UserRepository

router = APIRouter(prefix="/users", tags=["users"])

userRepository = UserRepository()

@router.get("/")
def list_users():
    return userRepository.list()

@router.post("/")
def create_user(user: UserModel):
    return userRepository.create(user)