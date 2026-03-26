from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  

class SalesOrder(Base):
    __tablename__ = "sales_orders"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer)

    customer_id = Column(Integer, ForeignKey("customers.id"))

    so_number = Column(String(20))
    order_date = Column(Date)

    total_amount = Column(Numeric(12, 2), default=0)
    tax_amount = Column(Numeric(12, 2), default=0)
    grand_total = Column(Numeric(12, 2), default=0)

    status = Column(String(20), default="DRAFT")

    customer = relationship("Customer", backref="sales_orders")

    items = relationship(
        "SalesOrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )