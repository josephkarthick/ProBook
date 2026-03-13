from sqlalchemy.orm import Session
from decimal import Decimal
from models.purchase_payment import PurchasePayment
from models.purchase_payment_allocation import PurchasePaymentAllocation
from models.purchase_bill import PurchaseBill
from models.account import Account
from models.vendor import Vendor
from services.journal_service import create_journal
from schemas.journal_schema import JournalEntryCreate, JournalLineCreate


@router.post("/purchase-payments/")
def create_vendor_payment(payment: VendorPaymentCreate, db: Session = Depends(get_db)):

    bill = db.query(PurchaseBill).filter(
        PurchaseBill.id == payment.purchase_bill_id
    ).first()

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    new_payment = VendorPayment(
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
    
balance = bill.grand_total - bill.paid_amount

if payment.amount > balance:
    raise HTTPException(
        status_code=400,
        detail="Payment exceeds remaining balance"
    )

new_payment = VendorPayment(
    company_id=bill.company_id,
    vendor_id=bill.vendor_id,
    purchase_bill_id=bill.id,
    payment_date=payment.payment_date,
    amount=payment.amount,
    payment_method=payment.payment_method
)  