from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from services.sales_order_service import create_sales_order

router = APIRouter(prefix="/api/sales-orders", tags=["Sales Order"])


@router.post("/")
def create_order(data: dict, db: Session = Depends(get_db)):
    return create_sales_order(db, data, company_id=1)


@router.get("/")
def list_orders():
    # optional: implement later
    return {"message": "list sales orders"}


@router.get("/{order_id}")
def get_order(order_id: int):
    # optional: implement later
    return {"message": f"sales order {order_id}"}