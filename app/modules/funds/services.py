from typing import List
from app.core.models.general_models import GenericResponse
from app.modules.funds.models import FundModel, FundResponseDto
from app.modules.funds.repository import FundsRepository


class FundService:
    def __init__(self):
        self.repository = FundsRepository()

    def create_fund(self, fund: FundModel) -> GenericResponse:
        if self.repository.find_by_name(fund.name):
            return GenericResponse[None](message="Fund already exists", status="error", data=None)
        fund_created = self.repository.save(fund)
        if fund_created is None:
            return GenericResponse[None](message="Fund creation failed", status="error", data=None)

        return GenericResponse[FundResponseDto](message="Fund created successfully", status="success", data=fund_created)

    def list_funds(self) -> GenericResponse:
        response = self.repository.list()
        data = response.get("Items", [])

        funds: List[FundResponseDto] = [FundResponseDto(**item) for item in data]
        safe_funds = [fund.model_dump(exclude={"password"}) for fund in funds]
        return GenericResponse[List[FundResponseDto]](message="Funds retrieved successfully", status="success", data=safe_funds)