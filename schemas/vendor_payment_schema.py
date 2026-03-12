from pydantic import BaseModel
from typing import List
from datetime import date


class PaymentAllocation(BaseModel):

    purchase_invoice_id: int
    amount: float


class VendorPaymentCreate(BaseModel):

    vendor_id: int
    payment_date: date
    payment_method: str
    reference: str
    description: str
    allocations: List[PaymentAllocation]