from sqlalchemy.orm import Session
from decimal import Decimal

from models.purchase_bill import PurchaseBill
from models.purchase_bill_item import PurchaseBillItem

from models.item import Item
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

    for item in data.items:

        subtotal = item.quantity * item.price
        tax = subtotal * item.gst_rate / 100
        total = subtotal + tax

        bill_item = PurchaseBillItem(
        
            purchase_id=bill.id,
            item_id=item.item_id,
            qty=item.quantity,
            rate=item.price,
            amount=subtotal,
            gst_rate=item.gst_rate,
            gst_amount=tax,
            total=total
        )

        db.add(bill_item)

        total_amount += subtotal
        tax_amount += tax

    bill.total_amount = total_amount
    bill.tax_amount = tax_amount
    bill.grand_total = total_amount + tax_amount
    bill.status = "POSTED"

    db.commit()
    db.refresh(bill)

    # 🔥 AUTO ACCOUNTING ENTRY
    create_purchase_journal(db, bill)

    return bill