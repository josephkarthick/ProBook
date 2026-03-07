from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from database import get_db
from core.template_engine import render_template

from models.sales_invoice import SalesInvoice
from models.sales_invoice_item import SalesInvoiceItem

router = APIRouter(tags=["Sales UI"])


# ===============================
# SALES LIST
# ===============================
@router.get("/sales")
def sales_list_page(request: Request):

    return render_template(
        "ProBook/Sales/sales_list.html",
        request
    )


# ===============================
# SALES CREATE
# ===============================
@router.get("/sales-create")
def sales_create_page(request: Request):

    return render_template(
        "ProBook/Sales/sales_create.html",
        request
    )


# ===============================
# SALES VIEW
# ===============================
@router.get("/sales-view/{invoice_id}")
def sales_view(
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
# SALES PRINT
# ===============================
@router.get("/sales-print/{invoice_id}")
def sales_print(
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