from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class ItemCategory(Base):

    __tablename__ = "item_categories"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    name = Column(String(150), nullable=False)

    parent_id = Column(Integer, ForeignKey("item_categories.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 🔹 self relationship for subcategories
    children = relationship("ItemCategory")