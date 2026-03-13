from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.purchase_bill import PurchaseBill
from models.purchase_payment import PurchasePayment
from schemas.purchase_payment_schema import PurchasePaymentCreate

router = APIRouter()


def generate_payment_ref(db: Session):

    last = db.query(PurchasePayment).order_by(
        PurchasePayment.id.desc()
    ).first()

    if not last:
        return "PAY-00001"

    num = int(last.reference_no.split("-")[1]) + 1
    return f"PAY-{num:05d}"


from services.journal_service import create_vendor_payment_journal

@router.post("/purchase-payments/")
def create_purchase_payment(payment: PurchasePaymentCreate, db: Session = Depends(get_db)):

    bill = db.query(PurchaseBill).filter(
        PurchaseBill.id == payment.purchase_bill_id
    ).first()

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    balance_before = bill.grand_total - (bill.paid_amount or 0)

    if payment.amount > balance_before:
        raise HTTPException(
            status_code=400,
            detail="Payment exceeds remaining balance"
        )

    balance_after = balance_before - payment.amount

    ref_no = generate_payment_ref(db)

    new_payment = PurchasePayment(

        company_id=bill.company_id,
        vendor_id=bill.vendor_id,
        purchase_bill_id=bill.id,

        reference_no=ref_no,
        payment_date=payment.payment_date,

        bill_total=bill.grand_total,
        amount_paid=payment.amount,
        balance_after=balance_after,

        payment_method=payment.payment_method
    )

    db.add(new_payment)
    db.flush()   # IMPORTANT so we get new_payment.id

    # CREATE JOURNAL ENTRY
    create_vendor_payment_journal(db, new_payment)

    # Update bill
    bill.paid_amount = (bill.paid_amount or 0) + payment.amount

    if bill.paid_amount == 0:
        bill.status = "UNPAID"
    elif bill.paid_amount < bill.grand_total:
        bill.status = "PARTIAL"
    else:
        bill.status = "PAID"

    db.commit()

    return {
        "message": "Payment recorded",
        "reference_no": ref_no,
        "balance_remaining": balance_after
    }
    
@router.get("/purchase-payments/{bill_id}")
def get_purchase_payments(bill_id: int, db: Session = Depends(get_db)):

    payments = (
        db.query(PurchasePayment)
        .filter(PurchasePayment.purchase_bill_id == bill_id)
        .order_by(PurchasePayment.id.desc())
        .all()
    )

    result = []

    for p in payments:
        result.append({
            "reference_no": p.reference_no,
            "payment_date": p.payment_date,
            "payment_method": p.payment_method,
            "amount_paid": float(p.amount_paid)
        })

    return result    