from fastapi import APIRouter

from app.modules.funds.models import FundModel
from app.modules.funds.services import FundService


router = APIRouter(prefix="/funds", tags=["Funds"])

fundService = FundService()

@router.post("/")
def create_fund(fund: FundModel):
    return fundService.create_fund(fund)

@router.get("/")
def list_funds():
    return fundService.list_funds()