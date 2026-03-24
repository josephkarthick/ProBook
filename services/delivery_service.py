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

    delivery_no = generate_delivery_no(db, company_id)

    sales_order_id = data.sales_order_id
    delivery_date = data.delivery_date or date.today()

    # ===============================
    # FETCH SALES ORDER
    # ===============================
    so = db.query(SalesOrder).filter(
        SalesOrder.id == sales_order_id,
        SalesOrder.company_id == company_id
    ).first()

    if not so:
        raise Exception("Sales Order not found")

    if so.status == "COMPLETED":
        raise Exception("Order already fully delivered")

    # ===============================
    # CREATE DELIVERY
    # ===============================
    delivery = DeliveryNote(
        company_id=company_id,
        sales_order_id=sales_order_id,
        delivery_no=delivery_no,
        delivery_date=delivery_date,
        status="POSTED"
    )

    db.add(delivery)
    db.flush()

    # ===============================
    # PROCESS ITEMS
    # ===============================
    for item in data.items:

        so_item = db.query(SalesOrderItem).filter(
            SalesOrderItem.id == item.order_item_id
        ).first()

        if not so_item:
            raise Exception("Order item not found")

        qty = Decimal(str(item.quantity))

        # 🔥 AVAILABLE QTY CHECK
        remaining_qty = Decimal(str(so_item.qty)) - Decimal(str(so_item.delivered_qty))

        if qty > remaining_qty:
            raise Exception(
                f"Cannot deliver more than remaining qty ({remaining_qty})"
            )

        # ===============================
        # CREATE DELIVERY ITEM
        # ===============================
        dn_item = DeliveryNoteItem(
            delivery_id=delivery.id,
            item_id=so_item.item_id,
            qty=qty
        )

        db.add(dn_item)

        # ===============================
        # 🔥 STOCK REDUCTION
        # ===============================
        reduce_stock_sale(
            db,
            company_id,
            so_item.item_id,
            float(qty),
            delivery.id
        )

        # ===============================
        # UPDATE SALES ORDER ITEM
        # ===============================
        so_item.delivered_qty = Decimal(str(so_item.delivered_qty)) + qty

    # ===============================
    # UPDATE SALES ORDER STATUS
    # ===============================
    all_delivered = True

    for so_item in so.items:
        if Decimal(str(so_item.delivered_qty)) < Decimal(str(so_item.qty)):
            all_delivered = False
            break

    if all_delivered:
        so.status = "COMPLETED"
    else:
        so.status = "PARTIAL"

    db.commit()
    db.refresh(delivery)

    return delivery