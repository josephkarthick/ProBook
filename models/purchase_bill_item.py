from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base


class PurchaseBillItem(Base):

    __tablename__ = "purchase_bill_items"

    id = Column(Integer, primary_key=True)

    purchase_id = Column(Integer, ForeignKey("purchase_bills.id"), nullable=False)

    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

    qty = Column(Numeric(10,2), nullable=False)

    rate = Column(Numeric(12,2), nullable=False)

    amount = Column(Numeric(12,2), nullable=False)

    gst_rate = Column(Numeric(5,2), default=0)

    gst_amount = Column(Numeric(12,2), default=0)

    total = Column(Numeric(12,2), nullable=False)

    purchase = relationship(
        "PurchaseBill",
        back_populates="items"
    )