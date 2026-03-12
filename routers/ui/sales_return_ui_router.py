from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from database import get_db
from core.template_engine import render_template

from models.sales_return import SalesReturn
from models.sales_return_item import SalesReturnItem

router = APIRouter(tags=["Sales Return UI"])


# ===============================
# SALES RETURN LIST
# ===============================
@router.get("/sales-returns")
def sales_return_list_page(request: Request):

    return render_template(
        "ProBook/Sales/sales_return_list.html",
        request
    )


# ===============================
# SALES RETURN CREATE
# ===============================
@router.get("/sales-return-create")
def sales_return_create_page(request: Request):

    return render_template(
        "ProBook/Sales/sales_return_create.html",
        request
    )


# ===============================
# SALES RETURN VIEW
# ===============================
@router.get("/sales-return-view/{return_id}")
def sales_return_view(
    return_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    return_doc = db.query(SalesReturn)\
        .filter(SalesReturn.id == return_id)\
        .first()

    items = db.query(SalesReturnItem)\
        .filter(SalesReturnItem.return_id == return_id)\
        .all()

    return render_template(
        "ProBook/Sales/sales_return_view.html",
        request,
        {
            "return_doc": return_doc,
            "items": items
        }
    )


# ===============================
# SALES RETURN PRINT
# ===============================
@router.get("/sales-return-print/{return_id}")
def sales_return_print(
    return_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    return_doc = db.query(SalesReturn)\
        .filter(SalesReturn.id == return_id)\
        .first()

    items = db.query(SalesReturnItem)\
        .filter(SalesReturnItem.return_id == return_id)\
        .all()

    return render_template(
        "ProBook/Sales/sales_return_print.html",
        request,
        {
            "return_doc": return_doc,
            "items": items
        }
    )