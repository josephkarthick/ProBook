from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from models.purchase_bill import PurchaseBill
from models.vendor import Vendor
from database import get_db
from core.company_utils import get_current_company_id

from schemas.purchase_schema import PurchaseBillCreate
from services.purchase_service import create_purchase_bill


router = APIRouter(prefix="/purchases", tags=["Purchases"])


# ===============================
# CREATE PURCHASE BILL
# ===============================
@router.post("/")
def create_purchase_api(
    data: PurchaseBillCreate,
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = get_current_company_id(request)

    return create_purchase_bill(db, data, company_id)


# ===============================
# LIST PURCHASE BILLS
# ===============================
@router.get("/")
def list_purchases(request: Request, db: Session = Depends(get_db)):

    company_id = get_current_company_id(request)

    purchases = (
        db.query(PurchaseBill)
        .join(Vendor, Vendor.id == PurchaseBill.vendor_id)
        .filter(PurchaseBill.company_id == company_id)
        .all()
    )

    result = []

    for p in purchases:

        paid_amount = float(p.paid_amount or 0)
        grand_total = float(p.grand_total)
        balance = grand_total - paid_amount

        result.append({
            "id": p.id,
            "bill_no": p.bill_no,
            "bill_date": p.bill_date,
            "vendor_name": p.vendor.name,

            "grand_total": grand_total,
            "paid_amount": paid_amount,
            "balance": balance,

            "status": p.status,

            # Needed for payment modal
            "vendor_id": p.vendor_id,
            "company_id": p.company_id
        })

    return result