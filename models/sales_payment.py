from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    # ✅ FK
    invoice_id = Column(Integer, ForeignKey("sales_invoices.id"))

    # ✅ FIXED (Numeric imported)
    amount = Column(Numeric(15, 2), nullable=False)

    mode = Column(String(20))
    notes = Column(String(255), nullable=True)
    date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # ✅ Relationship
    invoice = relationship("SalesInvoice", back_populates="payments")