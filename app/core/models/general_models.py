from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class GenericResponse(BaseModel, Generic[T]):
    message: str
    status: str
    data: T
