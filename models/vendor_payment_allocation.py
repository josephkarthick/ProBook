from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base

class VendorPaymentAllocation(Base):

    __tablename__ = "vendor_payment_allocations"

    id = Column(Integer, primary_key=True)

    payment_id = Column(Integer, ForeignKey("vendor_payments.id"))

    purchase_invoice_id = Column(
        Integer,
        ForeignKey("purchase_bills.id")
    )

    amount_applied = Column(Numeric(12,2))

    payment = relationship(
        "VendorPayment",
        back_populates="allocations"
    )