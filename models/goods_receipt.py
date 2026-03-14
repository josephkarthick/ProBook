from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class GoodsReceipt(Base):

    __tablename__ = "goods_receipts"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)

    grn_no = Column(String(50), nullable=False)

    receipt_date = Column(Date)

    status = Column(String(20), default="RECEIVED")

    items = relationship(
        "GoodsReceiptItem",
        back_populates="grn",
        cascade="all, delete-orphan"
    )