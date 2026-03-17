from pydantic import BaseModel
from typing import Optional

class StockAdjustmentSchema(BaseModel):
    item_id: int
    qty: float
    type: str
    reason: Optional[str] = None