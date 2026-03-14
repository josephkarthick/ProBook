from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base


class PurchaseOrderItem(Base):

    __tablename__ = "purchase_order_items"

    id = Column(Integer, primary_key=True)

    po_id = Column(Integer, ForeignKey("purchase_orders.id"))
    item_id = Column(Integer, ForeignKey("items.id"))

    quantity = Column(Numeric(12,2))
    price = Column(Numeric(12,2))
    gst_rate = Column(Numeric(5,2))
    total = Column(Numeric(12,2))

    # relationship
    po = relationship(
        "PurchaseOrder",
        back_populates="items"
    )