from sqlalchemy.orm import Session
from models.journal_entry import JournalEntry
from models.journal_line import JournalLine
from models.accounts import Account
from schemas.journal_schema import JournalEntryCreate


def create_journal(db: Session, data: JournalEntryCreate, company_id: int):

    if len(data.lines) < 2:
        raise ValueError("Journal must have at least 2 lines")

    total_debit = sum(line.debit for line in data.lines)
    total_credit = sum(line.credit for line in data.lines)

    if round(total_debit, 2) != round(total_credit, 2):
        raise ValueError("Debit and Credit must match")

    journal = JournalEntry(
        company_id=company_id,
        reference_no=data.reference_no,
        date=data.date,
        narration=data.narration,
        status="POSTED"
    )

    db.add(journal)
    db.flush()

    for line in data.lines:

        if line.debit > 0 and line.credit > 0:
            raise ValueError("Line cannot have both debit and credit")

        account = db.query(Account).filter(
            Account.id == line.account_id,
            Account.company_id == company_id
        ).first()

        if not account:
            raise ValueError("Invalid account for this company")

        db.add(
            JournalLine(
                journal_id=journal.id,
                account_id=line.account_id,
                debit=line.debit,
                credit=line.credit
            )
        )

    db.commit()
    db.refresh(journal)

    return journal