from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.purchase_bill import PurchaseBill
from models.purchase_bill_item import PurchaseBillItem
from models.company import Company
from decimal import Decimal
from datetime import datetime

router = APIRouter()


# -----------------------------
# GENERATE BILL NUMBER
# -----------------------------

def generate_bill_no(db: Session, company_id: int):

    last_bill = db.query(PurchaseBill)\
        .filter(PurchaseBill.company_id == company_id)\
        .order_by(PurchaseBill.id.desc())\
        .first()

    next_no = 1

    if last_bill:
        next_no = int(last_bill.bill_no.split("-")[-1]) + 1

    return f"PB-{next_no:05d}"


# -----------------------------
# CREATE PURCHASE
# -----------------------------

@router.post("/purchases/")
def create_purchase(data: dict, db: Session = Depends(get_db)):

    company_id = data.get("company_id")

    if not company_id:
        raise HTTPException(status_code=400, detail="Company required")

    vendor_id = data.get("vendor_id")
    bill_date = data.get("bill_date")
    items = data.get("items", [])

    if not items:
        raise HTTPException(status_code=400, detail="No items provided")

    # Generate bill number
    bill_no = generate_bill_no(db, company_id)

    subtotal = Decimal("0")
    tax_total = Decimal("0")

    purchase_items = []

    for i in items:

        qty = Decimal(str(i["quantity"]))
        price = Decimal(str(i["price"]))
        gst = Decimal(str(i["gst_rate"]))

        line_sub = qty * price
        tax = line_sub * gst / Decimal("100")
        total = line_sub + tax

        subtotal += line_sub
        tax_total += tax

        purchase_items.append(
            PurchaseBillItem(
                item_id=i["item_id"],
                quantity=qty,
                price=price,
                gst_rate=gst,
                total=total
            )
        )

    grand_total = subtotal + tax_total

    purchase = PurchaseBill(
        company_id=company_id,
        vendor_id=vendor_id,
        bill_no=bill_no,
        bill_date=bill_date,
        total_amount=subtotal,
        tax_amount=tax_total,
        grand_total=grand_total,
        paid_amount=0,
        status="UNPAID",
        items=purchase_items
    )

    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    return {
        "message": "Purchase created",
        "bill_no": bill_no
    }