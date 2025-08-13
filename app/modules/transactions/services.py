from typing import List
from app.core.models.general_models import GenericResponse
from app.modules.transactions.models import TransactionModel
from app.modules.transactions.repository import TransactionRepository


class TransactionService:
    def __init__(self):
        self.repository = TransactionRepository()

    def list_transactions(self, user_id: int, fund_id: int):
        response = self.repository.list(user_id, fund_id)
        data = response.get("Items", [])
        transactions: List[TransactionModel] = [TransactionModel(**item) for item in data]
        safe_transactions = [transaction.model_dump(exclude={"password"}) for transaction in transactions]
        return GenericResponse[List[TransactionModel]](message="Transactions retrieved successfully", status="success", data=safe_transactions)