# routes/payment.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.sales_payment import Payment
from models.sales import Sales

router = APIRouter(prefix="/api/payments", tags=["Payments"])


@router.post("/")
def create_payment(data: dict, db: Session = Depends(get_db)):

    invoice = db.query(Sales).filter(Sales.id == data["invoice_id"]).first()

    if not invoice:
        return {"detail": "Invoice not found"}

    # ✅ ADD HERE (VALIDATION BLOCK)
    amount = float(data.get("amount", 0))

    if amount <= 0:
        return {"detail": "Invalid amount"}

    if invoice.paid_amount + amount > invoice.total_amount:
        return {"detail": "Payment exceeds balance"}

    # ✅ CREATE PAYMENT
    payment = Payment(
        invoice_id=data["invoice_id"],
        amount=amount,
        mode=data.get("mode"),
        notes=data.get("notes")
    )

    db.add(payment)

    # ✅ UPDATE INVOICE
    invoice.paid_amount += amount
    invoice.balance_amount = invoice.total_amount - invoice.paid_amount

    # ✅ STATUS LOGIC (IMPROVED)
    if invoice.paid_amount <= 0:
        invoice.status = "UNPAID"
    elif invoice.paid_amount < invoice.total_amount:
        invoice.status = "PARTIAL"
    else:
        invoice.status = "PAID"

    db.commit()
    db.refresh(payment)

    return {"message": "Payment added successfully"}