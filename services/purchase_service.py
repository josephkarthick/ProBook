from sqlalchemy.orm import Session
from decimal import Decimal

from services.stock_service import add_stock_purchase
from models.purchase_bill import PurchaseBill
from models.purchase_bill_item import PurchaseBillItem
from services.journal_service import create_purchase_journal


def generate_bill_no(db, company_id):

    last = db.query(PurchaseBill)\
        .filter(PurchaseBill.company_id == company_id)\
        .order_by(PurchaseBill.id.desc())\
        .first()

    if not last:
        return "PB-00001"

    number = int(last.bill_no.split("-")[1]) + 1

    return f"PB-{number:05d}"


def create_purchase_bill(db: Session, data, company_id):

    bill_no = generate_bill_no(db, company_id)

    total_amount = Decimal("0")
    tax_amount = Decimal("0")

    bill = PurchaseBill(
        company_id=company_id,
        vendor_id=data.vendor_id,
        bill_no=bill_no,
        bill_date=data.bill_date
    )

    db.add(bill)
    db.flush()

    # ✅ correct
    po_id = data.po_id

    print("DEBUG PO:", po_id)

    for item in data.items:

        qty = Decimal(item.quantity)
        price = Decimal(item.price)
        gst_rate = Decimal(item.gst_rate)

        subtotal = qty * price
        tax = subtotal * gst_rate / Decimal("100")
        total = subtotal + tax

        bill_item = PurchaseBillItem(
            purchase_id=bill.id,
            item_id=item.item_id,
            qty=qty,
            rate=price,
            amount=subtotal,
            gst_rate=gst_rate,
            gst_amount=tax,
            total=total
        )

        db.add(bill_item)

        # ✅ ONLY manual bill adds stock
        if not po_id:
            add_stock_purchase(
                db=db,
                company_id=company_id,
                purchase_id=bill.id,
                item_id=item.item_id,
                qty=qty,
                cost=price
            )

        total_amount += subtotal
        tax_amount += tax

    bill.total_amount = total_amount
    bill.tax_amount = tax_amount
    bill.grand_total = total_amount + tax_amount
    bill.status = "POSTED"

    create_purchase_journal(db, bill)

    db.commit()
    db.refresh(bill)

    return bill