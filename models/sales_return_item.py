from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base


class SalesReturnItem(Base):

    __tablename__ = "sales_return_items"

    id = Column(Integer, primary_key=True)

    return_id = Column(Integer, ForeignKey("sales_returns.id"))

    invoice_item_id = Column(Integer, ForeignKey("sales_invoice_items.id"))

    item_id = Column(Integer, ForeignKey("items.id"))

    qty = Column(Numeric(10,2))

    price = Column(Numeric(12,2))

    amount = Column(Numeric(12,2))

    gst_rate = Column(Numeric(5,2))

    gst_amount = Column(Numeric(12,2))

    total = Column(Numeric(12,2))

    return_doc = relationship("SalesReturn", back_populates="items")