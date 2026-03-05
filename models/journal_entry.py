from sqlalchemy import Column, Integer, String, Date, ForeignKey
from datetime import date
from database import Base
from sqlalchemy.orm import relationship


class JournalEntry(Base):

    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    reference_no = Column(String(50))
    date = Column(Date, default=date.today)

    narration = Column(String(255))

    status = Column(String(20), default="POSTED")

    reversed_from_id = Column(Integer, ForeignKey("journal_entries.id"), nullable=True)

    lines = relationship(
        "JournalLine",
        back_populates="journal",
        cascade="all, delete-orphan"
    )