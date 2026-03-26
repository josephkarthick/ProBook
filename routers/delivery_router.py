from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models.sales_order import SalesOrder
from models.delivery_note import DeliveryNote
from services.delivery_service import create_delivery_note

router = APIRouter(prefix="/api/deliveries", tags=["Delivery"])


# ===============================
# GET SALES ORDER WITH ITEMS (FOR DELIVERY PAGE)
# ===============================
@router.get("/sales-order/{so_id}")
def get_sales_order(so_id: int, db: Session = Depends(get_db)):

    order = db.query(SalesOrder)\
        .options(joinedload(SalesOrder.items))\
        .filter(SalesOrder.id == so_id)\
        .first()

    if not order:
        raise HTTPException(status_code=404, detail="Sales Order not found")

    items = []

    for i in order.items:
        items.append({
            "id": i.id,
            "item_id": i.item_id,
            "item_name": i.item.name if i.item else f"Item {i.item_id}",
            "quantity": float(i.qty or 0),
            "delivered_qty": float(i.delivered_qty or 0),
            "price": float(i.price or 0),
            "gst_rate": float(i.gst_rate or 0)
        })

    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "customer_name": order.customer.name if order.customer else "",
        "items": items
    }


# ===============================
# CREATE DELIVERY
# ===============================
@router.post("/")
def create_delivery(data: dict, db: Session = Depends(get_db)):
    return create_delivery_note(db, data, company_id=1)


# ===============================
# LIST DELIVERIES (FOR LIST PAGE)
# ===============================
from sqlalchemy.orm import joinedload

@router.get("/")
def list_deliveries(db: Session = Depends(get_db)):

    deliveries = db.query(DeliveryNote)\
        .options(
            joinedload(DeliveryNote.sales_order)
            .joinedload(SalesOrder.customer)   # ✅ FIXED
        )\
        .order_by(DeliveryNote.id.desc())\
        .all()

    return [
        {
            "id": d.id,
            "delivery_no": d.delivery_no or "",
            "delivery_date": str(d.delivery_date) if d.delivery_date else "",
            "status": d.status or "DRAFT",
            "customer_name": (
                d.sales_order.customer.name
                if d.sales_order and d.sales_order.customer
                else "N/A"
            )
        }
        for d in deliveries
    ]


# ===============================
# GET SINGLE DELIVERY (OPTIONAL)
# ===============================


@router.get("/view/{delivery_id}")
def get_delivery(delivery_id: int, db: Session = Depends(get_db)):

    d = db.query(DeliveryNote)\
        .options(
            joinedload(DeliveryNote.sales_order)
            .joinedload(SalesOrder.items)   # 🔥 VERY IMPORTANT
        )\
        .filter(DeliveryNote.id == delivery_id)\
        .first()

    if not d:
        raise HTTPException(status_code=404, detail="Delivery not found")

    if not d.sales_order:
        raise HTTPException(status_code=400, detail="Sales Order not linked")

    so = d.sales_order

    items = []

    for i in so.items:

        delivered = float(i.delivered_qty or 0)
        invoiced = float(i.invoiced_qty or 0)

        pending_qty = delivered - invoiced

        print("DEBUG ITEM:", i.item_id, delivered, invoiced, pending_qty)

        if pending_qty <= 0:
            continue

        items.append({
            "item_id": i.item_id,
            "item_name": i.item.name if i.item else f"Item {i.item_id}",
            "quantity": pending_qty,
            "price": float(i.price or 0),
            "gst_rate": float(i.gst_rate or 0)
        })

    print("FINAL ITEMS:", items)   # 🔥 DEBUG

    return {
        "id": d.id,
        "customer_id": so.customer_id,
        "customer_name": so.customer.name if so.customer else "",
        "items": items
    }