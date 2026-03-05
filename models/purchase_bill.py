from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


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

    status = Column(String(20), default="POSTED")

    items = relationship(
        "PurchaseBillItem",
        back_populates="purchase",
        cascade="all, delete-orphan"
    )