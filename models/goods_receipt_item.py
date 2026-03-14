from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base


class GoodsReceiptItem(Base):

    __tablename__ = "goods_receipt_items"

    id = Column(Integer, primary_key=True)

    grn_id = Column(Integer, ForeignKey("goods_receipts.id"))

    item_id = Column(Integer, ForeignKey("items.id"))

    qty_received = Column(Numeric(10,2))

    grn = relationship(
        "GoodsReceipt",
        back_populates="items"
    )