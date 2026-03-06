from sqlalchemy import Column, Integer, ForeignKey, Numeric
from database import Base


class StockLayer(Base):

    __tablename__ = "stock_layers"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer, ForeignKey("companies.id"))

    item_id = Column(Integer, ForeignKey("items.id"))

    qty = Column(Numeric(10,2))

    cost = Column(Numeric(12,2))

    reference_id = Column(Integer)  # purchase bill