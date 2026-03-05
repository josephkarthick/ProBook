from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
from utils.template_helpers import render_template
from models.vendor import Vendor
from models.account import Account
from models.purchase_bill import PurchaseBill


router = APIRouter(prefix="/purchase-payment", tags=["Purchase Payment Page"])


@router.get("/", response_class=HTMLResponse)
def purchase_payment_page(request: Request, db: Session = Depends(get_db)):

    # ⚠ For now hardcode company_id = 1
    # Later we will move to session-based company isolation
    company_id = 1

    vendors = db.query(Vendor).filter(
        Vendor.company_id == company_id
    ).all()

    accounts = db.query(Account).filter(
        Account.company_id == company_id,
        Account.name.in_(["CASH", "BANK"])
    ).all()

    unpaid_bills = db.query(PurchaseBill).filter(
        PurchaseBill.company_id == company_id,
        PurchaseBill.total_amount > PurchaseBill.paid_amount
    ).all()

    return render_template(
        "VaisKart/Purchase/payment.html",
        request,
        vendors=vendors,
        accounts=accounts,
        unpaid_bills=unpaid_bills
    )