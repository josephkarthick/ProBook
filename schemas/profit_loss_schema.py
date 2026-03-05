from pydantic import BaseModel
from decimal import Decimal
from typing import List


class ProfitLossRow(BaseModel):

    account_id: int
    account_name: str
    amount: Decimal


class ProfitLossResponse(BaseModel):

    income: List[ProfitLossRow]
    expense: List[ProfitLossRow]

    total_income: Decimal
    total_expense: Decimal

    net_profit: Decimal