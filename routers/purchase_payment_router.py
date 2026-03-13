from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.purchase_bill import PurchaseBill
from models.purchase_payment import PurchasePayment
from schemas.purchase_payment_schema import PurchasePaymentCreate

router = APIRouter()


@router.post("/purchase-payments/")
def create_purchase_payment(payment: PurchasePaymentCreate, db: Session = Depends(get_db)):

    bill = db.query(PurchaseBill).filter(
        PurchaseBill.id == payment.purchase_bill_id
    ).first()

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    balance = bill.grand_total - bill.paid_amount

    if payment.amount > balance:
        raise HTTPException(
            status_code=400,
            detail="Payment exceeds remaining balance"
        )

    new_payment = PurchasePayment(
        company_id=bill.company_id,
        vendor_id=bill.vendor_id,
        purchase_bill_id=bill.id,
        payment_date=payment.payment_date,
        amount=payment.amount,
        payment_method=payment.payment_method
    )

    db.add(new_payment)

    bill.paid_amount += payment.amount

    if bill.paid_amount == 0:
        bill.status = "UNPAID"
    elif bill.paid_amount < bill.grand_total:
        bill.status = "PARTIAL"
    else:
        bill.status = "PAID"

    db.commit()

    return {"message": "Payment recorded"}