from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from utils.template_helpers import render_template
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from services.ledger_service import get_ledger

router = APIRouter()

@router.get("/accounting/ledger", response_class=HTMLResponse)
def ledger_page(request: Request):
    return render_template(
        "VaisKart/Accounting/ledger_report.html",
        request
    )
    


@router.get("/accounting/ledger/api/{account_id}")
def ledger_api(account_id: int, db: Session = Depends(get_db)):
    return get_ledger(db, account_id)    