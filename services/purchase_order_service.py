from sqlalchemy.orm import Session
from models.purchase_order import PurchaseOrder
from models.purchase_order_item import PurchaseOrderItem
import datetime


def create_purchase_order(db: Session, data):

    po_number = f"PO-{int(datetime.datetime.now().timestamp())}"

    subtotal = 0
    tax_total = 0

    po = PurchaseOrder(
        po_number=po_number,
        vendor_id=data.vendor_id,
        po_date=data.po_date,
        total_amount=0,
        status="DRAFT"
    )

    db.add(po)
    db.flush()

    for item in data.items:

        line_subtotal = item.quantity * item.price
        line_tax = line_subtotal * item.gst_rate / 100
        line_total = line_subtotal + line_tax

        subtotal += line_subtotal
        tax_total += line_tax

        po_item = PurchaseOrderItem(
            po_id=po.id,
            item_id=item.item_id,
            quantity=item.quantity,
            price=item.price,
            gst_rate=item.gst_rate,
            total=line_total
        )

        db.add(po_item)

    po.total_amount = subtotal + tax_total

    db.commit()
    db.refresh(po)

    return po