from sqlalchemy.orm import Session
from decimal import Decimal
from models.sales_order import SalesOrder
from models.sales_order_item import SalesOrderItem


def create_sales_order(db: Session, data, company_id):

    # =========================
    # INITIALIZE TOTALS
    # =========================
    total = Decimal("0.00")
    tax_total = Decimal("0.00")

    # =========================
    # AUTO SO NUMBER
    # =========================
    last = db.query(SalesOrder).order_by(SalesOrder.id.desc()).first()
    next_no = 1 if not last else last.id + 1
    so_number = f"SO-{str(next_no).zfill(3)}"

    # =========================
    # CREATE ORDER (NO COMMIT)
    # =========================
    order = SalesOrder(
        company_id=company_id,
        customer_id=data.get("customer_id"),
        so_number=so_number,
        order_date=data.get("order_date"),
        total_amount=0,
        tax_amount=0,
        grand_total=0,
        status="PENDING"
    )

    db.add(order)
    db.flush()   # ✅ get order.id safely

    # =========================
    # VALIDATION
    # =========================
    items = data.get("items", [])

    if not items:
        raise ValueError("Sales Order must have at least one item")

    # =========================
    # PROCESS ITEMS
    # =========================
    for item in items:

        item_id = (
            item.get("item_id") or
            item.get("product_id") or
            item.get("id")
        )

        if not item_id:
            raise ValueError(f"Missing item_id in item: {item}")

        qty = Decimal(str(item.get("qty") or item.get("quantity") or 0))
        price = Decimal(str(item.get("price") or item.get("rate") or 0))
        gst_rate = Decimal(str(item.get("gst_rate") or 0))

        if qty <= 0:
            raise ValueError(f"Invalid quantity in item: {item}")

        # =========================
        # CALCULATIONS
        # =========================
        amount = qty * price
        gst_amount = (amount * gst_rate) / Decimal("100")
        line_total = amount + gst_amount

        total += amount
        tax_total += gst_amount

        # =========================
        # SAVE ITEM
        # =========================
        db_item = SalesOrderItem(
            order_id=order.id,
            item_id=item_id,
            qty=qty,
            price=price,
            amount=amount,
            gst_rate=gst_rate,
            gst_amount=gst_amount,
            total=line_total
        )

        db.add(db_item)

    # =========================
    # FINAL TOTALS (CORRECT)
    # =========================
    order.total_amount = total
    order.tax_amount = tax_total   # ✅ use calculated GST
    order.grand_total = total + tax_total

    db.commit()
    db.refresh(order)

    return order
    
def list_sales_orders(db, company_id):

    orders = db.query(SalesOrder).filter(
        SalesOrder.company_id == company_id
    ).all()

    result = []

    for o in orders:
        result.append({
            "id": o.id,
            "so_number": o.so_number,
            "order_date": o.order_date.strftime("%Y-%m-%d") if o.order_date else None,
            "customer_id": o.customer_id,
            "customer_name": o.customer.name if o.customer else "",
            "total_amount": float(o.grand_total or 0),  # ✅ better
            "status": o.status or "PENDING"
        })

    return result    