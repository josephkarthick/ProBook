from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class ItemCreate(BaseModel):

    name: str
    category_id: Optional[int] = None
    unit: Optional[str] = "Nos"

    hsn_code: Optional[str] = None
    gst_rate: Optional[Decimal] = 0

    purchase_price: Optional[Decimal] = 0
    selling_price: Optional[Decimal] = 0

    track_inventory: Optional[bool] = True


class ItemUpdate(BaseModel):

    name: Optional[str] = None
    category_id: Optional[int] = None
    unit: Optional[str] = None

    hsn_code: Optional[str] = None
    gst_rate: Optional[Decimal] = None

    purchase_price: Optional[Decimal] = None
    selling_price: Optional[Decimal] = None

    track_inventory: Optional[bool] = None
    is_active: Optional[bool] = None