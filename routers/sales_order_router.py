from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from models.sales_order import SalesOrder
from models.sales_order_item import SalesOrderItem

from database import get_db
from core.company_utils import get_current_company_id

from services.sales_order_service import (
    create_sales_order,
    list_sales_orders
)

router = APIRouter(
    prefix="/api/sales-orders",
    tags=["Sales Order"]
)


# ===============================
# CREATE
# ===============================
@router.post("/")
def create_order(
    data: dict,
    request: Request,
    db: Session = Depends(get_db)
):
    company_id = get_current_company_id(request)
    return create_sales_order(db, data, company_id)


# ===============================
# LIST
# ===============================
@router.get("/")
def list_orders(
    request: Request,
    db: Session = Depends(get_db)
):
    company_id = get_current_company_id(request)
    return list_sales_orders(db, company_id)


# ===============================
# GET ONE
# ===============================
@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(SalesOrder).filter(
        SalesOrder.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Sales order not found"
        )

    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "customer_name": order.customer.name if order.customer else "",
        "status": order.status,
        "items": [
            {
                "id": i.id,
                "item_id": i.item_id,
                "item_name": i.item.name if i.item else "",
                "quantity": float(i.qty),
                "delivered_qty": float(i.delivered_qty or 0)
            }
            for i in order.items
        ]
    }


# ===============================
# CONFIRM ORDER
# ===============================
@router.put("/{order_id}/confirm")
def confirm_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(SalesOrder).filter(
        SalesOrder.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.status = "CONFIRMED"

    db.commit()

    return {
        "message": "Order confirmed"
    }