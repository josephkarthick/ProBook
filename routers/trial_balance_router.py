from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from services.trial_balance_service import get_trial_balance

router = APIRouter(prefix="/trial-balance", tags=["Trial Balance"])


@router.get("/")
def trial_balance(request: Request, db: Session = Depends(get_db)):

    company_id = request.session.get("company_id")

    return get_trial_balance(db, company_id)