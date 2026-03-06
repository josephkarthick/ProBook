from sqlalchemy.orm import Session
from models.journal_line import JournalLine
from models.journal_entry import JournalEntry


def get_account_ledger(db: Session, account_id, company_id, from_date, to_date):

    rows = (
        db.query(JournalLine)
        .join(JournalEntry, JournalEntry.id == JournalLine.journal_id)
        .filter(JournalLine.account_id == account_id)
        .filter(JournalEntry.company_id == company_id)
        .filter(JournalEntry.date >= from_date)
        .filter(JournalEntry.date <= to_date)
        .order_by(JournalEntry.date)
        .all()
    )

    result = []

    for r in rows:

        result.append({
            "date": r.journal.date,
            "description": r.journal.reference_no,
            "debit": float(r.debit),
            "credit": float(r.credit)
        })

    return result