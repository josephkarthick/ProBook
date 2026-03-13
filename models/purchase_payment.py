from sqlalchemy import Column, Integer, Date, Numeric, String, ForeignKey
from database import Base


class PurchasePayment(Base):

    __tablename__ = "purchase_payments"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    purchase_bill_id = Column(Integer, ForeignKey("purchase_bills.id"))

    reference_no = Column(String(30), unique=True)

    payment_date = Column(Date)

    bill_total = Column(Numeric(15,2))
    amount_paid = Column(Numeric(15,2))
    balance_after = Column(Numeric(15,2))

    payment_method = Column(String(50))