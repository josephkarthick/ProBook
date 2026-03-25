from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from database import get_db
from core.template_engine import render_template

# (Assuming you will create these models)
from models.sales_order import SalesOrder
from models.sales_order_item import SalesOrderItem

router = APIRouter(
    prefix="/sales",
    tags=["Sales Order UI"]
)


# ===============================
# ORDER LIST
# ===============================
@router.get("/order")
def order_list_page(request: Request):

    return render_template(
        "ProBook/Sales/sales_order_list.html",
        request
    )


# ===============================
# ORDER CREATE
# ===============================
@router.get("/order/create")
def order_create_page(request: Request):

    return render_template(
        "ProBook/Sales/sales_order_create.html",
        request
    )


# ===============================
# ORDER VIEW
# ===============================
@router.get("/order/{order_id}")
def order_view(
    order_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    order = db.query(SalesOrder)\
        .filter(SalesOrder.id == order_id)\
        .first()

    items = db.query(SalesOrderItem)\
        .filter(SalesOrderItem.order_id == order_id)\
        .all()

    return render_template(
        "ProBook/Sales/order_view.html",
        request,
        {
            "order": order,
            "items": items
        }
    )


# ===============================
# ORDER PRINT
# ===============================
@router.get("/order/{order_id}/print")
def order_print(
    order_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    order = db.query(SalesOrder)\
        .filter(SalesOrder.id == order_id)\
        .first()

    items = db.query(SalesOrderItem)\
        .filter(SalesOrderItem.order_id == order_id)\
        .all()

    return render_template(
        "ProBook/Sales/order_print.html",
        request,
        {
            "order": order,
            "items": items
        }
    )