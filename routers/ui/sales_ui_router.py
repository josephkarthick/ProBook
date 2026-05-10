from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from core.template_engine import render_template

from models.company import Company
from models.sales_invoice import SalesInvoice
from models.sales_invoice_item import SalesInvoiceItem

router = APIRouter(
    prefix="/sales",
    tags=["Sales UI"]
)


# ===============================
# INVOICE LIST
# ===============================
@router.get("/invoice")
def invoice_list_page(request: Request):

    return render_template(
        "ProBook/Sales/sales_list.html",
        request
    )


# ===============================
# INVOICE CREATE
# ===============================
@router.get("/invoice/create")
def invoice_create_page(request: Request):

    return render_template(
        "ProBook/Sales/sales_create.html",
        request
    )


# ===============================
# INVOICE VIEW
# ===============================
@router.get("/invoice/{invoice_id}")
def invoice_view(
    invoice_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    # ================= INVOICE =================
    invoice = db.query(SalesInvoice).filter(
        SalesInvoice.id == invoice_id
    ).first()

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    # ================= ITEMS =================
    items = db.query(SalesInvoiceItem).filter(
        SalesInvoiceItem.invoice_id == invoice_id
    ).all()

    # ================= COMPANY =================
    company = None

    if invoice.company_id:

        company = db.query(Company).filter(
            Company.id == invoice.company_id
        ).first()

    return render_template(
        "ProBook/Sales/sales_view.html",
        request,
        {
            "invoice": invoice,
            "items": items,
            "company": company
        }
    )


# ===============================
# INVOICE PRINT
# ===============================
@router.get("/invoice/{invoice_id}/print")
def invoice_print(
    invoice_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    # ================= INVOICE =================
    invoice = db.query(SalesInvoice).filter(
        SalesInvoice.id == invoice_id
    ).first()

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    # ================= ITEMS =================
    items = db.query(SalesInvoiceItem).filter(
        SalesInvoiceItem.invoice_id == invoice_id
    ).all()

    # ================= COMPANY =================
    company = None

    if invoice.company_id:

        company = db.query(Company).filter(
            Company.id == invoice.company_id
        ).first()

    return render_template(
        "ProBook/Sales/sales_print.html",
        request,
        {
            "invoice": invoice,
            "items": items,
            "company": company
        }
    )