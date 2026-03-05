from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from utils.template_helpers import render_template
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from services.ledger_service import get_ledger

router = APIRouter()

@router.get("/accounting/balance-sheet", response_class=HTMLResponse)
def balance_sheet_page(request: Request):
    return render_template(
        "VaisKart/Accounting/balance_sheet.html",
        request
    )