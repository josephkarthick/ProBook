from pydantic import BaseModel, EmailStr
from typing import Optional


class CompanyBase(BaseModel):
    name: str
    code: str

    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None

    gst_number: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    id: int

    class Config:
        from_attributes = True   # (Pydantic v2)