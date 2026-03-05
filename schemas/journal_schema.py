from pydantic import BaseModel
from typing import List
from decimal import Decimal
from datetime import date


# -----------------------------
# Journal Line
# -----------------------------
class JournalLineCreate(BaseModel):
    account_id: int
    debit: Decimal = 0
    credit: Decimal = 0


class JournalLineResponse(BaseModel):
    account_id: int
    account_name: str
    debit: Decimal
    credit: Decimal

    class Config:
        from_attributes = True


# -----------------------------
# Journal Entry
# -----------------------------
class JournalEntryCreate(BaseModel):
    reference_no: str | None = None
    date: date
    narration: str | None = None
    lines: List[JournalLineCreate]


class JournalEntryResponse(BaseModel):
    id: int
    reference_no: str
    date: date
    narration: str | None
    status: str

    class Config:
        from_attributes = True