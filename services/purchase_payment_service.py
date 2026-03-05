from sqlalchemy.orm import Session
from decimal import Decimal
from models.purchase_payment import PurchasePayment
from models.purchase_payment_allocation import PurchasePaymentAllocation
from models.purchase_bill import PurchaseBill
from models.account import Account
from models.vendor import Vendor
from services.journal_service import create_journal
from schemas.journal_schema import JournalEntryCreate, JournalLineCreate


def create_purchase_payment(db: Session, payment_data):

    try:
        total_payment = Decimal(payment_data.total_amount)
        remaining_amount = total_payment

        # 1️⃣ Validate Vendor
        vendor = db.query(Vendor).filter(
            Vendor.id == payment_data.vendor_id,
            Vendor.company_id == payment_data.company_id
        ).first()

        if not vendor or not vendor.account_id:
            raise Exception("Vendor not found or liability account missing")

        # 2️⃣ Create Payment Header
        payment = PurchasePayment(
            company_id=payment_data.company_id,
            vendor_id=payment_data.vendor_id,
            payment_date=payment_data.payment_date,
            payment_mode=payment_data.payment_mode,
            reference_no=payment_data.reference_no,
            total_amount=total_payment
        )

        db.add(payment)
        db.flush()

        # 3️⃣ Get Unpaid Bills (Oldest First)
        bills = db.query(PurchaseBill).filter(
            PurchaseBill.company_id == payment_data.company_id,
            PurchaseBill.vendor_id == payment_data.vendor_id,
            PurchaseBill.total_amount > PurchaseBill.paid_amount
        ).order_by(PurchaseBill.bill_date.asc()).all()

        for bill in bills:
            if remaining_amount <= 0:
                break

            outstanding = bill.total_amount - bill.paid_amount
            allocate_amount = min(outstanding, remaining_amount)

            # Create Allocation
            allocation = PurchasePaymentAllocation(
                company_id=payment_data.company_id,
                payment_id=payment.id,
                purchase_id=bill.id,
                allocated_amount=allocate_amount
            )

            db.add(allocation)

            # Update Bill
            bill.paid_amount += allocate_amount

            if bill.paid_amount == bill.total_amount:
                bill.status = "PAID"
            else:
                bill.status = "PARTIAL"

            remaining_amount -= allocate_amount

        # 4️⃣ Get Cash/Bank Account
        payment_account = db.query(Account).filter(
            Account.company_id == payment_data.company_id,
            Account.name.ilike(f"%{payment_data.payment_mode}%")
        ).first()

        if not payment_account:
            raise Exception("Payment account not found")

        # 5️⃣ Create Journal Entry
        journal_data = JournalEntryCreate(
            company_id=payment_data.company_id,
            date=payment_data.payment_date,
            reference_no=payment_data.reference_no,
            narration=f"Purchase Payment - {payment_data.reference_no}",
            lines=[
                JournalLineCreate(
                    account_id=vendor.account_id,
                    debit=total_payment,
                    credit=Decimal("0")
                ),
                JournalLineCreate(
                    account_id=payment_account.id,
                    debit=Decimal("0"),
                    credit=total_payment
                )
            ]
        )

        create_journal(db, journal_data)

        db.commit()
        db.refresh(payment)

        return payment

    except Exception as e:
        db.rollback()
        raise