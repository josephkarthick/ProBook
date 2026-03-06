from sqlalchemy import Column, Integer, ForeignKey, Date, Numeric, String
from sqlalchemy.orm import relationship
from database import Base


class SalesInvoice(Base):

    __tablename__ = "sales_invoices"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer, ForeignKey("companies.id"))

    customer_id = Column(Integer, ForeignKey("customers.id"))

    invoice_no = Column(String(20))

    invoice_date = Column(Date)

    total_amount = Column(Numeric(12,2))
    tax_amount = Column(Numeric(12,2))
    grand_total = Column(Numeric(12,2))

    status = Column(String(20), default="POSTED")

    items = relationship(
        "SalesInvoiceItem",
        back_populates="invoice",
        cascade="all, delete-orphan"
    )