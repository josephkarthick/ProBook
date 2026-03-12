from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class PurchaseBill(Base):

    __tablename__ = "purchase_bills"

    __table_args__ = (
        UniqueConstraint("company_id", "bill_no", name="uq_company_purchase_bill"),
    )

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)

    bill_no = Column(String(50), nullable=False)

    bill_date = Column(Date, nullable=False)

    total_amount = Column(Numeric(15,2), default=0)

    tax_amount = Column(Numeric(15,2), default=0)

    grand_total = Column(Numeric(15,2), default=0)

    paid_amount = Column(Numeric(15,2), default=0)

    # UNPAID | PARTIALLY_PAID | PAID
    status = Column(String(20), default="UNPAID")

    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship(
        "PurchaseBillItem",
        back_populates="purchase",
        cascade="all, delete-orphan"
    )

    vendor = relationship("Vendor")

    # Useful property for balance
    @property
    def balance_amount(self):
        return float(self.grand_total or 0) - float(self.paid_amount or 0)