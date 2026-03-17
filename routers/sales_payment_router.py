from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.sales_payment import Payment
from models.sales_invoice import SalesInvoice
from datetime import datetime
from decimal import Decimal
from num2words import num2words

router = APIRouter(prefix="/api/payments", tags=["Payments"])


# ================= CREATE PAYMENT =================
@router.post("/")
def create_payment(data: dict, db: Session = Depends(get_db)):

    invoice = db.query(SalesInvoice).filter(
        SalesInvoice.id == data.get("invoice_id")
    ).first()

    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    # ✅ Validate amount
    if "amount" not in data:
        raise HTTPException(status_code=400, detail="Amount is required")

    try:
        amount = Decimal(str(data["amount"]))
    except:
        raise HTTPException(status_code=400, detail="Invalid amount")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")

    # ✅ Safe Decimal handling
    paid_amount = Decimal(str(invoice.paid_amount or 0))
    grand_total = Decimal(str(invoice.grand_total or 0))
    balance_amount = Decimal(str(invoice.balance_amount or grand_total))

    # ❌ Prevent overpayment
    if amount > balance_amount:
        raise HTTPException(status_code=400, detail="Amount exceeds balance")

    # ✅ Save payment
    payment = Payment(
        invoice_id=invoice.id,
        amount=amount,
        mode=data.get("mode", "Cash"),
        notes=data.get("notes", ""),
        date=datetime.now()
    )

    db.add(payment)

    # ✅ Update invoice
    new_paid = paid_amount + amount
    new_balance = grand_total - new_paid

    # 🔒 Fix floating edge (0.000 issue)
    if new_balance < Decimal("0.01"):
        new_balance = Decimal("0.00")

    invoice.paid_amount = new_paid
    invoice.balance_amount = new_balance

    # ✅ Status update
    if new_balance == 0:
        invoice.payment_status = "PAID"
    elif new_paid > 0:
        invoice.payment_status = "PARTIAL"
    else:
        invoice.payment_status = "UNPAID"

    db.commit()

    return {
        "message": "Payment added",
        "paid": float(new_paid),
        "balance": float(new_balance),
        "status": invoice.payment_status
    }


# ================= GET PAYMENTS =================
@router.get("/{invoice_id}")
def get_payments(invoice_id: int, db: Session = Depends(get_db)):

    payments = db.query(Payment).filter(
        Payment.invoice_id == invoice_id
    ).order_by(Payment.date.desc()).all()

    return [
        {
            "date": p.date.strftime("%Y-%m-%d") if p.date else "",
            "amount": float(p.amount),
            "mode": p.mode or "",
            "notes": p.notes or ""
        }
        for p in payments
    ]