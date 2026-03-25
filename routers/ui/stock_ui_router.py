from fastapi import APIRouter, Request
from core.template_engine import render_template

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory UI"]
)


# ===============================
# STOCK SUMMARY
# ===============================
@router.get("/summary")
def stock_summary_page(request: Request):
    return render_template(
        "ProBook/Inventory/stock_summary.html",
        request
    )


# ===============================
# STOCK LEDGER
# ===============================
@router.get("/ledger")
def stock_ledger_page(request: Request):
    return render_template(
        "ProBook/Inventory/stock_ledger.html",
        request
    )


# ===============================
# STOCK ADJUSTMENT
# ===============================
@router.get("/adjustment")
def stock_adjustment_page(request: Request):
    return render_template(
        "ProBook/Inventory/stock_adjustment.html",
        request
    )


# ===============================
# LOW STOCK
# ===============================
@router.get("/low-stock")
def low_stock_page(request: Request):
    return render_template(
        "ProBook/Inventory/low_stock.html",
        request
    )