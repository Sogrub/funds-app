from typing import Optional
from fastapi import APIRouter, Query
from app.modules.transactions.services import TransactionService


router = APIRouter(prefix="/transactions", tags=["Transactions"])

transactionService = TransactionService()

@router.get("/")
def list_transactions(
    user_id: Optional[int] = Query(None),
    fund_id: Optional[int] = Query(None)
):
    return transactionService.list_transactions(user_id, fund_id)