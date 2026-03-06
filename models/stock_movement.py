from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime
from sqlalchemy.sql import func
from database import Base


class StockMovement(Base):

    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer, ForeignKey("companies.id"))

    item_id = Column(Integer, ForeignKey("items.id"))

    qty = Column(Numeric(10,2))

    movement_type = Column(String(20))  # PURCHASE / SALE / ADJUSTMENT

    reference_id = Column(Integer)  # purchase_id / sale_id

    created_at = Column(DateTime(timezone=True), server_default=func.now())