from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)

    company_id = Column(Integer, ForeignKey("companies.id"))

    name = Column(String(200), nullable=False)

    phone = Column(String(20))

    email = Column(String(200))

    address = Column(String(500))

    gst_number = Column(String(50))