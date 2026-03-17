from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.sales_invoice import SalesInvoice
from models.sales_payment import Payment
from models.customer import Customer

router = APIRouter(prefix="/api/ledger", tags=["Ledger"])


@router.get("/{customer_id}")
def customer_ledger(customer_id: int, request: Request, db: Session = Depends(get_db)):

    company_id = request.session.get("company_id")

    if not company_id:
        raise HTTPException(status_code=400, detail="Company not selected")

    # ================= GET INVOICES =================
    invoices = db.query(SalesInvoice).filter(
        SalesInvoice.customer_id == customer_id,
        SalesInvoice.company_id == company_id
    ).all()

    # ================= GET PAYMENTS =================
    payments = db.query(Payment).join(
        SalesInvoice, Payment.invoice_id == SalesInvoice.id
    ).filter(
        SalesInvoice.customer_id == customer_id,
        SalesInvoice.company_id == company_id
    ).all()

    # ================= MERGE =================
    ledger = []

    for inv in invoices:
        ledger.append({
            "date": inv.invoice_date,
            "type": "Invoice",
            "ref": inv.invoice_no,
            "debit": float(inv.grand_total),
            "credit": 0
        })

    for p in payments:
        ledger.append({
            "date": p.date,
            "type": "Payment",
            "ref": f"PAY-{p.invoice_id}",
            "debit": 0,
            "credit": float(p.amount)
        })

    # ================= SORT BY DATE =================
    ledger.sort(key=lambda x: x["date"])

    # ================= RUNNING BALANCE =================
    balance = 0

    for row in ledger:
        balance += row["debit"] - row["credit"]
        row["balance"] = round(balance, 2)

    return ledger