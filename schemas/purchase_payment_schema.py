# schemas/purchase_payment_schema.py

from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class PurchasePaymentCreate(BaseModel):

    purchase_bill_id: int
    payment_date: date
    amount: Decimal
    payment_method: str