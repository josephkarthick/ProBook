from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from core.company_utils import get_current_company_id

from models.journal_entry import JournalEntry
from models.journal_line import JournalLine
from services.journal_service import create_journal
from schemas.journal_schema import JournalEntryCreate

from datetime import date

router = APIRouter(prefix="/journals", tags=["Journals"])


# ===============================
# CREATE JOURNAL
# ===============================
@router.post("/")
def create_journal_api(
    data: JournalEntryCreate,
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = get_current_company_id(request)

    try:
        return create_journal(db, data, company_id)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ===============================
# LIST JOURNALS
# ===============================
@router.get("/")
def list_journals(
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = get_current_company_id(request)

    journals = db.query(JournalEntry)\
        .filter(JournalEntry.company_id == company_id)\
        .all()

    result = []

    for j in journals:

        total_debit = sum(line.debit for line in j.lines)
        total_credit = sum(line.credit for line in j.lines)

        result.append({
            "id": j.id,
            "date": j.date,
            "reference_no": j.reference_no,
            "narration": j.narration,
            "total_debit": float(total_debit),
            "total_credit": float(total_credit),
            "status": j.status
        })

    return result


# ===============================
# GET SINGLE JOURNAL
# ===============================
@router.get("/{journal_id}")
def get_journal(
    journal_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = get_current_company_id(request)

    journal = db.query(JournalEntry)\
        .filter(
            JournalEntry.id == journal_id,
            JournalEntry.company_id == company_id
        ).first()

    if not journal:
        raise HTTPException(status_code=404, detail="Journal not found")

    return {
        "id": journal.id,
        "date": journal.date,
        "reference_no": journal.reference_no,
        "narration": journal.narration,
        "status": journal.status,
        "lines": [
            {
                "account_name": line.account.name,
                "debit": float(line.debit),
                "credit": float(line.credit)
            }
            for line in journal.lines
        ]
    }


# ===============================
# REVERSE JOURNAL
# ===============================
@router.post("/{journal_id}/reverse")
def reverse_journal(
    journal_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    company_id = get_current_company_id(request)

    original = db.query(JournalEntry)\
        .filter(
            JournalEntry.id == journal_id,
            JournalEntry.company_id == company_id
        ).first()

    if not original:
        raise HTTPException(status_code=404, detail="Journal not found")

    if original.status == "REVERSED":
        raise HTTPException(status_code=400, detail="Journal already reversed")

    reverse_entry = JournalEntry(
        company_id=company_id,
        reference_no=f"REV-{original.reference_no}",
        date=date.today(),
        narration=f"Reversal of {original.reference_no}",
        status="POSTED",
        reversed_from_id=original.id
    )

    db.add(reverse_entry)
    db.flush()

    for line in original.lines:

        db.add(
            JournalLine(
                journal_id=reverse_entry.id,
                account_id=line.account_id,
                debit=line.credit,
                credit=line.debit
            )
        )

    original.status = "REVERSED"

    db.commit()

    return {"message": "Journal reversed successfully"}