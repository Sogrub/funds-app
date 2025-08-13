from enum import Enum
from unicodedata import category
from pydantic import BaseModel

class CategoryEnum(str, Enum):
    FPV = "FPV"
    FIC = "FIC"

class FundModel(BaseModel):
    name: str
    category: CategoryEnum
    min_amount: int

class FundResponseDto(BaseModel):
    id: int
    name: str
    category: CategoryEnum
    min_amount: int