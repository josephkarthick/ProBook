from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    icon = Column(String(100))
    url = Column(String(200))

    parent_id = Column(Integer, ForeignKey("menus.id"), nullable=True)
    order_no = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    parent = relationship(
        "Menu",
        remote_side=[id],
        back_populates="submenu"
    )

    submenu = relationship(
        "Menu",
        back_populates="parent",
        order_by="Menu.order_no",
        lazy="selectin"
    )