from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from num2words import num2words
from database import get_db
from models.sales_invoice import SalesInvoice
from models.customer import Customer

from schemas.sales_schema import SalesInvoiceCreate
from services.sales_service import create_sales_invoice

router = APIRouter(prefix="/api/sales", tags=["Sales"])


# ===============================
# LIST SALES
# ===============================
@router.get("/")
def list_sales(request: Request, db: Session = Depends(get_db)):

    company_id = request.session.get("company_id")

    if not company_id:
        raise HTTPException(status_code=400, detail="Company not selected")

    sales = db.query(
        SalesInvoice.id,
        SalesInvoice.invoice_no,
        SalesInvoice.invoice_date,
        SalesInvoice.grand_total,
        SalesInvoice.payment_status,   # ✅ FIXED
        Customer.name.label("customer_name")
    ).join(
        Customer, Customer.id == SalesInvoice.customer_id
    ).filter(
        SalesInvoice.company_id == company_id
    ).order_by(
        SalesInvoice.id.desc()
    ).all()

    result = []

    for s in sales:
        result.append({
            "id": s.id,
            "invoice_no": s.invoice_no,
            "invoice_date": s.invoice_date.strftime("%Y-%m-%d"),
            "grand_total": float(s.grand_total),

            # ✅ IMPORTANT FIX
            "payment_status": s.payment_status if s.payment_status else "UNPAID",

            "customer_name": s.customer_name
        })

    return result


# ===============================
# CREATE SALES
# ===============================
@router.post("/")
def create_sales_api(
    data: SalesInvoiceCreate,
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = request.session.get("company_id")

    if not company_id:
        raise HTTPException(status_code=400, detail="Company not selected")

    return create_sales_invoice(
        db=db,
        data=data,
        company_id=company_id
    )