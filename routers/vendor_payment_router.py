from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from database import get_db
from schemas.vendor_payment_schema import VendorPaymentCreate
from services.vendor_payment_service import create_vendor_payment

router = APIRouter(prefix="/api", tags=["Vendor Payments"])


@router.post("/vendor-payments")
def create_payment(
    data: VendorPaymentCreate,
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = request.session.get("company_id")

    result = create_vendor_payment(db, data, company_id)

    return {
        "status": "success",
        "payment_no": result.payment_no
    }