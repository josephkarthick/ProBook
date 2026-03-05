from pydantic import BaseModel
from decimal import Decimal
from typing import List


class BalanceSheetRow(BaseModel):

    account_id: int
    account_name: str
    amount: Decimal


class BalanceSheetResponse(BaseModel):

    assets: List[BalanceSheetRow]
    liabilities: List[BalanceSheetRow]
    equity: List[BalanceSheetRow]

    total_assets: Decimal
    total_liabilities: Decimal
    total_equity: Decimal