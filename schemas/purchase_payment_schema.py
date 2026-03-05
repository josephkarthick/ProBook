from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class PurchasePaymentCreate(BaseModel):
    company_id: int
    vendor_id: int
    payment_date: date
    payment_mode: str
    reference_no: str
    total_amount: Decimal