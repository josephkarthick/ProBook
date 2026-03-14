from pydantic import BaseModel
from datetime import date
from typing import List


class PurchaseOrderItemCreate(BaseModel):
    item_id: int
    quantity: float
    price: float
    gst_rate: float


class PurchaseOrderCreate(BaseModel):
    vendor_id: int
    po_date: date
    items: List[PurchaseOrderItemCreate]