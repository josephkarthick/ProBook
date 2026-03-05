from sqlalchemy import Column, Integer, ForeignKey, Numeric
from database import Base
from sqlalchemy.orm import relationship


class JournalLine(Base):

    __tablename__ = "journal_lines"

    id = Column(Integer, primary_key=True, index=True)

    journal_id = Column(Integer, ForeignKey("journal_entries.id"), nullable=False)

    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)

    debit = Column(Numeric(12,2), default=0)
    credit = Column(Numeric(12,2), default=0)

    journal = relationship("JournalEntry", back_populates="lines")

    account = relationship("Account")