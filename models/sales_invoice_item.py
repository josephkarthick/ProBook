from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base


class SalesInvoiceItem(Base):

    __tablename__ = "sales_invoice_items"

    id = Column(Integer, primary_key=True)

    invoice_id = Column(Integer, ForeignKey("sales_invoices.id"))

    item_id = Column(Integer, ForeignKey("items.id"))

    qty = Column(Numeric(10,2))

    price = Column(Numeric(12,2))

    amount = Column(Numeric(12,2))

    gst_rate = Column(Numeric(5,2))

    gst_amount = Column(Numeric(12,2))

    total = Column(Numeric(12,2))

    invoice = relationship(
        "SalesInvoice",
        back_populates="items"
    )