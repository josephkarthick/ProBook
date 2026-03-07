from pydantic import BaseModel
from typing import Optional


class CustomerCreate(BaseModel):

    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    gst_number: Optional[str] = None


class CustomerResponse(BaseModel):

    id: int
    name: str
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    gst_number: Optional[str]

    class Config:
        from_attributes = True