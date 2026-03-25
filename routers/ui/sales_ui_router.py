from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from database import get_db
from core.template_engine import render_template

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

    invoice = db.query(SalesInvoice)\
        .filter(SalesInvoice.id == invoice_id)\
        .first()

    items = db.query(SalesInvoiceItem)\
        .filter(SalesInvoiceItem.invoice_id == invoice_id)\
        .all()

    return render_template(
        "ProBook/Sales/sales_view.html",
        request,
        {
            "invoice": invoice,
            "items": items
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

    invoice = db.query(SalesInvoice)\
        .filter(SalesInvoice.id == invoice_id)\
        .first()

    items = db.query(SalesInvoiceItem)\
        .filter(SalesInvoiceItem.invoice_id == invoice_id)\
        .all()

    return render_template(
        "ProBook/Sales/sales_print.html",
        request,
        {
            "invoice": invoice,
            "items": items
        }
    )