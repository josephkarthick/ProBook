from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    item_code = Column(String(20), nullable=False)

    name = Column(String(150), nullable=False)

    description = Column(String(255))

    # 🔹 Category reference
    category_id = Column(Integer, ForeignKey("item_categories.id"))

    unit = Column(String(20), default="Nos")

    hsn_code = Column(String(20))

    gst_rate = Column(Numeric(5,2), default=0)

    purchase_price = Column(Numeric(12,2), default=0)

    selling_price = Column(Numeric(12,2), default=0)

    track_inventory = Column(Boolean, default=True)

    reorder_level = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 🔹 Relationship
    category = relationship("ItemCategory")
    
    min_stock_level = Column(Numeric(10,2), default=0)