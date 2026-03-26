from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import date

from models.delivery_note import DeliveryNote
from models.delivery_note_item import DeliveryNoteItem
from models.sales_order import SalesOrder
from models.sales_order_item import SalesOrderItem

from services.stock_service import reduce_stock_sale


# ===============================
# GENERATE DELIVERY NUMBER
# ===============================
def generate_delivery_no(db, company_id):

    last = db.query(DeliveryNote)\
        .filter(DeliveryNote.company_id == company_id)\
        .order_by(DeliveryNote.id.desc())\
        .first()

    if not last:
        return "DN-00001"

    number = int(last.delivery_no.split("-")[1]) + 1
    return f"DN-{number:05d}"


# ===============================
# CREATE DELIVERY NOTE
# ===============================
def create_delivery_note(db: Session, data, company_id):

    if not data.get("items"):
        raise HTTPException(status_code=400, detail="No items provided")

    delivery_no = generate_delivery_no(db, company_id)

    sales_order_id = data["sales_order_id"]
    delivery_date = data.get("delivery_date") or date.today()

    so = db.query(SalesOrder).filter(
        SalesOrder.id == sales_order_id,
        SalesOrder.company_id == company_id
    ).first()

    if not so:
        raise HTTPException(status_code=404, detail="Sales Order not found")

    if so.status == "COMPLETED":
        raise HTTPException(status_code=400, detail="Already delivered")

    delivery = DeliveryNote(
        company_id=company_id,
        sales_order_id=sales_order_id,
        delivery_no=delivery_no,
        delivery_date=delivery_date,
        status="POSTED"
    )

    db.add(delivery)
    db.flush()

    for item in data["items"]:

        so_item = db.query(SalesOrderItem).filter(
            SalesOrderItem.id == item["order_item_id"],
            SalesOrderItem.order_id == sales_order_id
        ).first()

        if not so_item:
            raise HTTPException(status_code=404, detail="Order item not found")

        qty = Decimal(str(item["quantity"]))

        remaining_qty = Decimal(str(so_item.qty)) - Decimal(str(so_item.delivered_qty))

        if qty > remaining_qty:
            raise HTTPException(
                status_code=400,
                detail=f"Max allowed qty is {remaining_qty}"
            )

        db.add(DeliveryNoteItem(
            delivery_id=delivery.id,
            item_id=so_item.item_id,
            qty=qty
        ))

        reduce_stock_sale(
            db,
            company_id,
            so_item.item_id,
            float(qty),
            delivery.id
        )

        so_item.delivered_qty = Decimal(str(so_item.delivered_qty)) + qty

    # status update
    all_delivered = all(
        Decimal(str(i.delivered_qty)) >= Decimal(str(i.qty))
        for i in so.items
    )

    so.status = "COMPLETED" if all_delivered else "PARTIAL"

    db.commit()
    db.refresh(delivery)

    return delivery