from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
from database import engine, Base
from core.template_engine import render_template

# Routers
from routers.auth_router import router as auth_router
from routers.company_router import router as company_router
from routers.account_router import router as account_router
from routers.account_page_router import router as account_page_router
from routers.journal_router import router as journal_router
from routers.ledger_router import router as ledger_router
from routers.trial_balance_router import router as trial_balance_router
from routers.profit_loss_router import router as profit_loss_router
from routers.balance_sheet_router import router as balance_sheet_router
from routers.vendor_router import router as vendor_router
from routers.vendor_page_router import router as vendor_page_router
from routers.category_router import router as category_router
from routers.purchase_router import router as purchase_router
from routers.purchase_page_router import router as purchase_page_router
from routers.ui.item_ui_router import router as item_ui_router
from routers.item_router import router as item_router
from routers.ui.journal_ui_router import router as journal_ui_router
from routers.ui.ledger_ui_router import router as ledger_ui_router
from routers.ui.trial_balance_ui_router import router as trial_balance_ui_router
from routers.ui.profit_loss_ui_router import router as profit_loss_ui_router
from routers.ui.balance_sheet_ui_router import router as balance_sheet_ui_router
from routers.ui.purchase_ui_router import router as purchase_ui_router
from routers.stock_router import router as stock_router
from routers.ui.stock_ui_router import router as stock_ui_router
from routers.ui.company_ui_router import router as company_ui_router
from routers.ui.vendor_ui_router import router as vendor_ui_router
from routers.sales_router import router as sales_router
from routers.ui.sales_ui_router import router as sales_ui_router
from routers.ui.customer_ui_router import router as customer_ui_router
from routers.customer_router import router as customer_router
from routers.purchase_payment_router import router as purchase_payment_router
from routers.ui.purchase_payment_ui_router import router as purchase_payment_ui_router
from routers.ui.grn_ui_router import router as grn_ui_router
from routers.grn_router import router as grn_router
from routers.purchase_order_router import router as po_router
from routers.ui.po_ui_router import router as po_ui_router
from routers.sales_payment_router import router as sales_payment_router
from routers.customer_ledger_router import router as customer_ledger_router
from routers.ui.customer_ledger_ui_router import router as customer_ledger_ui_router




app = FastAPI()

# Session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="probook-secret-key"
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create tables
Base.metadata.create_all(bind=engine)


# ======================
# Register Routers
# ======================

app.include_router(auth_router)
app.include_router(company_router)

app.include_router(account_router)
app.include_router(account_page_router)

app.include_router(journal_router)
app.include_router(ledger_router)
app.include_router(trial_balance_router)
app.include_router(profit_loss_router)
app.include_router(balance_sheet_router)

app.include_router(vendor_router)
app.include_router(vendor_page_router)

app.include_router(category_router)

app.include_router(purchase_router)
app.include_router(purchase_page_router)

app.include_router(item_router)
app.include_router(item_ui_router)

app.include_router(journal_ui_router)
app.include_router(ledger_ui_router)
app.include_router(trial_balance_ui_router)
app.include_router(profit_loss_ui_router)
app.include_router(balance_sheet_ui_router)

app.include_router(purchase_ui_router)
app.include_router(purchase_payment_router)
app.include_router(purchase_payment_ui_router)


app.include_router(stock_router)
app.include_router(stock_ui_router)

app.include_router(company_ui_router)

app.include_router(vendor_ui_router)

app.include_router(sales_router)
app.include_router(sales_ui_router)

app.include_router(customer_router)
app.include_router(customer_ui_router)

app.include_router(grn_ui_router)
app.include_router(grn_router)


app.include_router(po_router)
app.include_router(po_ui_router)

app.include_router(sales_payment_router)


app.include_router(customer_ledger_router)


app.include_router(customer_ledger_ui_router)

# ======================
# Home Page
# ======================

@app.get("/")
def home(request: Request):

    if not request.session.get("user_id"):
        return RedirectResponse("/login")

    return render_template(
        "ProBook/Base/base.html",
        request
    )


# ======================
# Company Page
# ======================

@app.get("/company")
def company_page(request: Request):

    return render_template(
        "ProBook/settings/companies.html",
        request
    )


# ======================
# Debug Routes
# ======================

@app.get("/routes")
def list_routes():

    routes = []

    for route in app.routes:
        routes.append(route.path)

    return routes