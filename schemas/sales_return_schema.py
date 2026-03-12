from pydantic import BaseModel
from typing import List
from datetime import date


class SalesReturnItem(BaseModel):

    invoice_item_id: int
    item_id: int
    quantity: float
    price: float
    gst_rate: float


class SalesReturnCreate(BaseModel):

    invoice_id: int
    return_date: date
    items: List[SalesReturnItem]