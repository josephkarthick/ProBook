from sqlalchemy import Column, Integer, Date, Numeric, String, ForeignKey
from database import Base


class PurchasePayment(Base):

    __tablename__ = "purchase_payments"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id"))

    vendor_id = Column(Integer, ForeignKey("vendors.id"))

    purchase_bill_id = Column(Integer, ForeignKey("purchase_bills.id"))

    payment_date = Column(Date)

    amount = Column(Numeric(15,2))

    payment_method = Column(String(50))