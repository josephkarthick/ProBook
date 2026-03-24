from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base


class DeliveryNoteItem(Base):

    __tablename__ = "delivery_note_items"

    id = Column(Integer, primary_key=True)

    delivery_id = Column(Integer, ForeignKey("delivery_notes.id"))
    item_id = Column(Integer, ForeignKey("items.id"))

    qty = Column(Numeric(10, 2))

    # 🔗 RELATION
    delivery = relationship("DeliveryNote", back_populates="items")