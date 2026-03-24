from sqlalchemy.orm import Session
from decimal import Decimal

from models.sales_order import SalesOrder
from models.sales_order_item import SalesOrderItem


def create_sales_order(db: Session, data, company_id):

    order = SalesOrder(
        company_id=company_id,
        customer_id=data["customer_id"],
        order_no="SO-001",  # improve later
        order_date=data["order_date"],
        total_amount=0,
        tax_amount=0,
        grand_total=0,
        status="CONFIRMED"
    )

    db.add(order)
    db.flush()

    total = Decimal("0")
    tax_total = Decimal("0")

    for item in data["items"]:

        qty = Decimal(str(item["quantity"]))
        price = Decimal(str(item["price"]))
        gst = Decimal(str(item["gst_rate"]))

        subtotal = qty * price
        tax = subtotal * gst / 100
        grand = subtotal + tax

        db.add(SalesOrderItem(
            order_id=order.id,
            item_id=item["item_id"],
            qty=qty,
            price=price,
            amount=subtotal,
            gst_rate=gst,
            gst_amount=tax,
            total=grand
        ))

        total += subtotal
        tax_total += tax

    order.total_amount = total
    order.tax_amount = tax_total
    order.grand_total = total + tax_total

    db.commit()
    db.refresh(order)

    return order