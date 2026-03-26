from sqlalchemy import Column, Integer, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship
from database import Base
from models.item import Item 

class SalesOrderItem(Base):
    __tablename__ = "sales_order_items"

    id = Column(Integer, primary_key=True)

    order_id = Column(Integer, ForeignKey("sales_orders.id"))
    item_id = Column(Integer, ForeignKey("items.id"))

    qty = Column(Numeric(10, 2))
    price = Column(Numeric(10, 2))

    amount = Column(Numeric(12, 2))
    gst_rate = Column(Numeric(5, 2))
    gst_amount = Column(Numeric(12, 2))
    total = Column(Numeric(12, 2))

    # 🚚 DELIVERY TRACKING
    delivered_qty = Column(Numeric(10,2), default=0)

    # 💰 INVOICE TRACKING
    invoiced_qty = Column(Numeric(10,2), default=0)

    # 🔗 RELATION
    order = relationship("SalesOrder", back_populates="items")
    
    status = Column(String(20), default="PENDING")
    item = relationship("Item")