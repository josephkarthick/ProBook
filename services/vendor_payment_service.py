from sqlalchemy.orm import Session
from decimal import Decimal

from models.vendor_payment import VendorPayment
from models.vendor_payment_allocation import VendorPaymentAllocation
from models.purchase_bill import  PurchaseBill
from services.journal_service import create_vendor_payment_journal


def generate_payment_no(db, company_id):

    last = db.query(VendorPayment)\
        .filter(VendorPayment.company_id == company_id)\
        .order_by(VendorPayment.id.desc())\
        .first()

    if not last:
        return "VP-00001"

    num = int(last.payment_no.split("-")[1]) + 1

    return f"VP-{num:05d}"


def create_vendor_payment(db: Session, data, company_id):

    payment_no = generate_payment_no(db, company_id)

    total_amount = Decimal("0")

    payment = VendorPayment(
        company_id=company_id,
        vendor_id=data.vendor_id,
        payment_no=payment_no,
        payment_date=data.payment_date,
        payment_method=data.payment_method,
        reference=data.reference,
        description=data.description
    )

    db.add(payment)
    db.flush()

    for a in data.allocations:

        amount = Decimal(a.amount)

        invoice = db.query(PurchaseInvoice)\
            .filter(PurchaseInvoice.id == a.purchase_invoice_id)\
            .first()

        if amount > invoice.balance_amount:
            raise Exception("Cannot pay more than bill balance")

        alloc = VendorPaymentAllocation(
            payment_id=payment.id,
            purchase_invoice_id=a.purchase_invoice_id,
            amount_applied=amount
        )

        db.add(alloc)

        invoice.paid_amount += amount
        invoice.balance_amount -= amount

        if invoice.balance_amount == 0:
            invoice.status = "PAID"
        else:
            invoice.status = "PARTIALLY_PAID"

        total_amount += amount

    payment.total_amount = total_amount

    db.commit()

    create_vendor_payment_journal(db, payment)

    return payment