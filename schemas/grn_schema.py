from pydantic import BaseModel
from datetime import date
from typing import List


class GRNItem(BaseModel):

    item_id: int
    qty: float


class GRNCreate(BaseModel):

    po_id: int
    receipt_date: date
    items: List[GRNItem]


class GRNList(BaseModel):

    id: int
    grn_no: str
    receipt_date: date
    vendor_name: str
    status: str
    total_items: int
    total_qty: float