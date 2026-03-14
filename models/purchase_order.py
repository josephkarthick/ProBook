from sqlalchemy import Column, Integer, Date, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class PurchaseOrder(Base):

    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True)

    po_number = Column(String(50))
    vendor_id = Column(Integer, ForeignKey("vendors.id"))

    po_date = Column(Date)

    total_amount = Column(Numeric(12,2))
    status = Column(String(20))

    items = relationship(
        "PurchaseOrderItem",
        back_populates="po",
        cascade="all, delete-orphan"
    )