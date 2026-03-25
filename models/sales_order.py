from sqlalchemy import Column, Date, Integer, Numeric, String
from sqlalchemy.orm import relationship

from database import Base


class SalesOrder(Base):
    __tablename__ = "sales_orders"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer)
    customer_id = Column(Integer)

    order_no = Column(String(20))
    order_date = Column(Date)

    total_amount = Column(Numeric(12, 2))
    tax_amount = Column(Numeric(12, 2))
    grand_total = Column(Numeric(12, 2))

    status = Column(String(20), default="DRAFT")

    items = relationship(
        "SalesOrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
