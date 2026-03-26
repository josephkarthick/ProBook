from pydantic import BaseModel
from decimal import Decimal
from typing import List, Optional
from datetime import date


class PurchaseItemCreate(BaseModel):

    item_id: int
    quantity: Decimal
    price: Decimal
    gst_rate: Decimal


class PurchaseBillCreate(BaseModel):

    vendor_id: int
    bill_date: date

    # 🔥 ADD THIS LINE
    po_id: Optional[int] = None

    items: List[PurchaseItemCreate]


class PurchaseBillResponse(BaseModel):

    id: int
    bill_no: str
    vendor_id: int
    bill_date: date
    total_amount: Decimal
    tax_amount: Decimal
    grand_total: Decimal

    class Config:
        from_attributes = True