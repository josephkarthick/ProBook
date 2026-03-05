from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from decimal import Decimal

from models.journal_entry import JournalEntry
from models.journal_line import JournalLine


def get_account_ledger(
    db: Session,
    account_id: int,
    company_id: int,
    from_date: date,
    to_date: date
):

    # ----------------------------
    # 1️⃣ Opening Balance
    # ----------------------------
    opening = db.query(
        func.sum(JournalLine.debit).label("debit"),
        func.sum(JournalLine.credit).label("credit")
    ).join(JournalEntry)\
     .filter(
        JournalLine.account_id == account_id,
        JournalEntry.company_id == company_id,
        JournalEntry.date < from_date
    ).first()

    opening_debit = opening.debit or Decimal("0")
    opening_credit = opening.credit or Decimal("0")

    balance = opening_debit - opening_credit

    ledger = []

    # Add opening row
    ledger.append({
        "date": from_date,
        "reference_no": "OPENING",
        "narration": "Opening Balance",
        "debit": opening_debit,
        "credit": opening_credit,
        "balance": balance
    })

    # ----------------------------
    # 2️⃣ Fetch Transactions
    # ----------------------------
    rows = db.query(
        JournalEntry.date,
        JournalEntry.reference_no,
        JournalEntry.narration,
        JournalLine.debit,
        JournalLine.credit
    ).join(JournalEntry)\
     .filter(
        JournalLine.account_id == account_id,
        JournalEntry.company_id == company_id,
        JournalEntry.date >= from_date,
        JournalEntry.date <= to_date
    )\
     .order_by(JournalEntry.date)\
     .all()

    # ----------------------------
    # 3️⃣ Running Balance
    # ----------------------------
    for r in rows:

        balance += r.debit
        balance -= r.credit

        ledger.append({
            "date": r.date,
            "reference_no": r.reference_no,
            "narration": r.narration,
            "debit": r.debit,
            "credit": r.credit,
            "balance": balance
        })

    return ledger