from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class LedgerRow(BaseModel):

    date: date
    reference_no: str | None
    narration: str | None

    debit: Decimal
    credit: Decimal

    balance: Decimal