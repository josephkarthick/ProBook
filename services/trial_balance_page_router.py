from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from utils.template_helpers import render_template
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from services.ledger_service import get_ledger

router = APIRouter()


@router.get("/accounting/trial-balance", response_class=HTMLResponse)
def trial_balance_page(request: Request):
    return render_template(
        "VaisKart/Accounting/trial_balance.html",
        request
    )