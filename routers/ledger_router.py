from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from datetime import date

from database import get_db
from services.ledger_service import get_account_ledger

router = APIRouter(prefix="/ledger", tags=["Ledger"])


@router.get("/{account_id}")
def account_ledger(
    account_id: int,
    request: Request,
    from_date: date,
    to_date: date,
    db: Session = Depends(get_db)
):

    company_id = request.session.get("company_id")

    return get_account_ledger(
        db,
        account_id,
        company_id,
        from_date,
        to_date
    )
    
    @router.get("/{account_id}")
def get_ledger(account_id: int, db: Session = Depends(get_db)):

    rows = (
        db.query(JournalLine)
        .join(JournalEntry, JournalEntry.id == JournalLine.journal_id)
        .filter(JournalLine.account_id == account_id)
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