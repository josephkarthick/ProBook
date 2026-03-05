from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


# 🔹 Create Account
class AccountCreate(BaseModel):

    name: str
    account_code: Optional[str] = None

    account_type: Optional[str] = None
    # ASSET, LIABILITY, INCOME, EXPENSE, EQUITY

    parent_id: Optional[int] = None

    is_group: bool = False

    opening_balance: Optional[Decimal] = 0
    opening_type: Optional[str] = None   # DEBIT / CREDIT


# 🔹 Update Account
class AccountUpdate(BaseModel):

    name: Optional[str] = None
    account_code: Optional[str] = None

    account_type: Optional[str] = None

    parent_id: Optional[int] = None

    is_group: Optional[bool] = None

    opening_balance: Optional[Decimal] = None
    opening_type: Optional[str] = None


# 🔹 Response Schema
class AccountResponse(BaseModel):

    id: int
    company_id: int

    name: str
    account_code: Optional[str]

    account_type: Optional[str]

    parent_id: Optional[int]

    is_group: bool
    is_system: bool

    opening_balance: Decimal
    opening_type: Optional[str]

    class Config:
        from_attributes = True