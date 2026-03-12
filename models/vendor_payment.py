from sqlalchemy import Column, Integer, ForeignKey, String, Date, Numeric
from sqlalchemy.orm import relationship
from database import Base


class VendorPayment(Base):

    __tablename__ = "vendor_payments"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer, ForeignKey("companies.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"))

    payment_no = Column(String(20))
    payment_date = Column(Date)

    payment_method = Column(String(20))
    reference = Column(String(100))
    description = Column(String(255))

    total_amount = Column(Numeric(12,2))

    allocations = relationship("VendorPaymentAllocation", back_populates="payment")