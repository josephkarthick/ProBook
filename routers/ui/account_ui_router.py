from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db
from core.template_engine import render_template
from models.accounts import Account
from core.company_utils import get_current_company_id

router = APIRouter(prefix="/accounting/accounts", tags=["Accounts UI"])


def build_account_tree(accounts):
    lookup = {}
    tree = []

    for acc in accounts:
        acc.children = []
        lookup[acc.id] = acc

    for acc in accounts:
        if acc.parent_id:
            parent = lookup.get(acc.parent_id)
            if parent:
                parent.children.append(acc)
        else:
            tree.append(acc)

    return tree


@router.get("/", response_class=HTMLResponse)
def account_page(request: Request, db: Session = Depends(get_db)):

    company_id = get_current_company_id(request)

    accounts = db.query(Account)\
        .filter(Account.company_id == company_id)\
        .all()

    tree_accounts = build_account_tree(accounts)

    return render_template(
        "ProBook/Accounts/accounts.html",
        request,
        {
            "accounts": tree_accounts
        }
    )