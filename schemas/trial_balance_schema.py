from pydantic import BaseModel
from decimal import Decimal
from typing import List


class TrialBalanceRow(BaseModel):
    account_id: int
    account_name: str
    debit: Decimal
    credit: Decimal


class TrialBalanceResponse(BaseModel):
    rows: List[TrialBalanceRow]
    total_debit: Decimal
    total_credit: Decimal