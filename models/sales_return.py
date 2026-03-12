from sqlalchemy import Column, Integer, ForeignKey, Numeric, Date, String
from sqlalchemy.orm import relationship
from database import Base


class SalesReturn(Base):

    __tablename__ = "sales_returns"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer, ForeignKey("companies.id"))

    invoice_id = Column(Integer, ForeignKey("sales_invoices.id"))

    return_no = Column(String(20))

    return_date = Column(Date)

    total_amount = Column(Numeric(12,2))

    tax_amount = Column(Numeric(12,2))

    grand_total = Column(Numeric(12,2))

    reason = Column(String(255))

    items = relationship("SalesReturnItem", back_populates="return_doc")