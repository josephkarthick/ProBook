from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Boolean
from database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    account_code = Column(String(20), nullable=True)     

    name = Column(String(150), nullable=False)

    # Only root groups will have account_type
    account_type = Column(String(20), nullable=True)
    # ASSET, LIABILITY, INCOME, EXPENSE, EQUITY

    parent_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)

    is_group = Column(Boolean, default=False)

    is_system = Column(Boolean, default=False)
    # Prevent deletion of system accounts

    opening_balance = Column(Numeric(12, 2), default=0)
    opening_type = Column(String(10))  # DEBIT / CREDIT