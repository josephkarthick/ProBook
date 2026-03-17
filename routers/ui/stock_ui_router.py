from fastapi import APIRouter, Request
from core.template_engine import render_template

router = APIRouter(prefix="/stock", tags=["Stock UI"])


# ===============================
# STOCK SUMMARY
# ===============================
@router.get("/summary")
def stock_summary_page(request: Request):
    return render_template(
        "ProBook/Stock/stock_summary.html",
        request
    )


# ===============================
# STOCK LEDGER
# ===============================
@router.get("/ledger")
def stock_ledger_page(request: Request):
    return render_template(
        "ProBook/Stock/stock_ledger.html",
        request
    )


# ===============================
# STOCK ADJUSTMENT
# ===============================
@router.get("/adjustment")
def stock_adjustment_page(request: Request):
    return render_template(
        "ProBook/Stock/stock_adjustment.html",
        request
    )
    
@router.get("/low-stock")
def low_stock_page(request: Request):
    return render_template(
        "ProBook/Stock/low_stock.html",
        request
    )    