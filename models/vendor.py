from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Vendor(Base):

    __tablename__ = "vendors"

    __table_args__ = (
        UniqueConstraint("company_id", "vendor_code", name="uq_vendor_company_code"),
    )

    id = Column(Integer, primary_key=True, index=True)

    # 🔹 Multi-company isolation
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)

    # 🔹 Vendor Ledger (Accounts Payable)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)

    # 🔹 Vendor unique code per company
    vendor_code = Column(String(20), nullable=False, index=True)

    name = Column(String(150), nullable=False)

    contact_person = Column(String(150))

    phone = Column(String(20), nullable=False)
    email = Column(String(150))

    gst_number = Column(String(50))

    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(20))

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    account = relationship("Account")

    # 🔹 Helper property
    @property
    def account_name(self):
        return self.account.name if self.account else None