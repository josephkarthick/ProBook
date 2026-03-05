from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime





class VendorCreate(BaseModel):

    vendor_code: str
    name: str
    contact_person: Optional[str] = None
    phone: str
    email: Optional[str] = None
    gst_number: Optional[str] = None

    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None


class VendorUpdate(BaseModel):

    name: Optional[str] = None
    contact_person: Optional[str] = None

    phone: Optional[str] = None
    email: Optional[EmailStr] = None

    gst_number: Optional[str] = None

    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None

    account_id: Optional[int] = None

    is_active: Optional[bool] = None


class VendorResponse(BaseModel):

    id: int
    company_id: int

    vendor_code: str
    name: str
    contact_person: Optional[str]

    phone: str
    email: Optional[str]

    gst_number: Optional[str]

    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    pincode: Optional[str]

    account_id: int
    account_name: Optional[str]

    is_active: bool

    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True