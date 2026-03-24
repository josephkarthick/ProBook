from sqlalchemy import Column, Integer, ForeignKey, Date, String
from sqlalchemy.orm import relationship
from database import Base


class DeliveryNote(Base):

    __tablename__ = "delivery_notes"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer, ForeignKey("companies.id"))
    sales_order_id = Column(Integer, ForeignKey("sales_orders.id"))

    delivery_no = Column(String(20))
    delivery_date = Column(Date)

    status = Column(String(20), default="POSTED")

    # 🔗 RELATION
    items = relationship(
        "DeliveryNoteItem",
        back_populates="delivery",
        cascade="all, delete-orphan"
    )

    sales_order = relationship("SalesOrder", backref="deliveries")