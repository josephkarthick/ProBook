from sqlalchemy import Column, Integer, ForeignKey, Date, Numeric, String
from sqlalchemy.orm import relationship
from database import Base   # 🔥 THIS WAS MISSING

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
    
    # DRAFT / CONFIRMED / PARTIAL / COMPLETED