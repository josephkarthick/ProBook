from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from core.template_engine import render_template

router = APIRouter(tags=["Stock UI"])


@router.get("/stock-summary")
def stock_summary_page(request: Request):

    return render_template(
        "ProBook/Stock/stock_summary.html",
        request
    )


@router.get("/stock-ledger")
def stock_ledger_page(request: Request):

    return render_template(
        "ProBook/Stock/stock_ledger.html",
        request
    )    