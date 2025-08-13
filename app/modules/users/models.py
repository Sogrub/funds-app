from typing import Optional
from pydantic import BaseModel

class UserModel(BaseModel):
    name: str
    email: str
    password: str

class UserResponseDto(BaseModel):
    id: int
    name: str
    email: str
    balance: int