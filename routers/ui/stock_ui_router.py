from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from core.template_engine import render_template

router = APIRouter()


@router.get("/stock-report", response_class=HTMLResponse)
def stock_report_page(request: Request):

    return render_template(
        "ProBook/Stock/stock_report.html",
        request
    )