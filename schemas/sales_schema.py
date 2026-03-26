from pydantic import BaseModel
from decimal import Decimal
from typing import List, Optional
from datetime import date


class SalesItemCreate(BaseModel):

    item_id: int
    quantity: Decimal
    price: Decimal
    gst_rate: Decimal


class SalesInvoiceCreate(BaseModel):

    customer_id: int
    invoice_date: date

    # 🔥 ADD THESE TWO LINES
    source_type: Optional[str] = None
    source_id: Optional[int] = None

    items: List[SalesItemCreate]