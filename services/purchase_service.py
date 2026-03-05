from sqlalchemy.orm import Session
from decimal import Decimal

from models.purchase_bill import PurchaseBill
from models.purchase_bill_item import PurchaseBillItem
from decimal import Decimal
from models.purchase_bill import PurchaseBill
from models.purchase_bill_item import PurchaseBillItem

def generate_purchase_bill_no(db, company_id):

    last_bill = (
        db.query(PurchaseBill)
        .filter(PurchaseBill.company_id == company_id)
        .order_by(PurchaseBill.id.desc())
        .first()
    )

    if not last_bill:
        return "PB-00001"

    last_number = int(last_bill.bill_no.split("-")[1])

    new_number = last_number + 1

    return f"PB-{new_number:05d}"
    


def create_purchase_bill(db, data, company_id):

    bill_no = generate_purchase_bill_no(db, company_id)

    total_amount = Decimal("0")
    tax_amount = Decimal("0")

    purchase = PurchaseBill(
        company_id=company_id,
        vendor_id=data.vendor_id,
        bill_no=bill_no,
        bill_date=data.bill_date
    )

    db.add(purchase)
    db.flush()

    for item in data.items:

        amount = item.qty * item.rate

        gst = amount * item.gst_rate / Decimal("100")

        total = amount + gst

        line = PurchaseBillItem(
            purchase_id=purchase.id,
            item_id=item.item_id,
            qty=item.qty,
            rate=item.rate,
            amount=amount,
            gst_rate=item.gst_rate,
            gst_amount=gst,
            total=total
        )

        total_amount += amount
        tax_amount += gst

        db.add(line)

    purchase.total_amount = total_amount
    purchase.tax_amount = tax_amount
    purchase.grand_total = total_amount + tax_amount

    db.commit()
    db.refresh(purchase)

    return purchase    