from sqlalchemy.orm import Session
from sqlalchemy import func
from models.journal_line import JournalLine
from models.journal_entry import JournalEntry
from models.accounts import Account


def get_trial_balance(db: Session, company_id: int):

    rows = db.query(
        Account.id,
        Account.name,
        func.sum(JournalLine.debit).label("debit"),
        func.sum(JournalLine.credit).label("credit")
    ).join(JournalLine, JournalLine.account_id == Account.id)\
     .join(JournalEntry, JournalEntry.id == JournalLine.journal_id)\
     .filter(JournalEntry.company_id == company_id)\
     .group_by(Account.id, Account.name)\
     .all()

    result = []

    for r in rows:

        debit = r.debit or 0
        credit = r.credit or 0

        if debit == 0 and credit == 0:
            continue

        result.append({
            "account_id": r.id,
            "name": r.name,   # FIXED
            "debit": float(debit),
            "credit": float(credit)
        })

    return result