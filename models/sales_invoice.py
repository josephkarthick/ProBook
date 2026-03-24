from sqlalchemy import Column, Integer, ForeignKey, Date, Numeric, String
from sqlalchemy.orm import relationship
from database import Base
from models.sales_payment import Payment

class SalesInvoice(Base):

    __tablename__ = "sales_invoices"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer, ForeignKey("companies.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))

    # 🔗 LINK TO SALES ORDER (NEW)
    sales_order_id = Column(Integer, ForeignKey("sales_orders.id"), nullable=True)

    invoice_no = Column(String(20))
    invoice_date = Column(Date)

    # 💰 AMOUNTS
    total_amount = Column(Numeric(12,2), default=0)
    tax_amount = Column(Numeric(12,2), default=0)
    grand_total = Column(Numeric(12,2), default=0)

    # 💳 PAYMENT TRACKING
    paid_amount = Column(Numeric(12,2), default=0)
    balance_amount = Column(Numeric(12,2), default=0)
    payment_status = Column(String(20), default="UNPAID")

    # 📌 STATUS
    status = Column(String(20), default="POSTED")

    # 🔗 RELATIONSHIPS
    payments = relationship(
        Payment,
        back_populates="invoice",
        cascade="all, delete-orphan"
    )

    items = relationship(
        "SalesInvoiceItem",
        back_populates="invoice",
        cascade="all, delete-orphan"
    )

    # 🔗 OPTIONAL RELATION TO SALES ORDER
    sales_order = relationship("SalesOrder", backref="invoices")