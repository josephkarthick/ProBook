from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from database import get_db
from core.template_engine import render_template
from models.accounts import Account
from core.company_utils import get_current_company_id

router = APIRouter()


# 🔥 Build hierarchical tree structure
def build_account_tree(accounts):

    lookup = {}
    tree = []

    # Prepare lookup dictionary
    for acc in accounts:
        acc.children = []  # dynamic attribute
        lookup[acc.id] = acc

    # Build tree
    for acc in accounts:
        if acc.parent_id:
            parent = lookup.get(acc.parent_id)
            if parent:
                parent.children.append(acc)
        else:
            tree.append(acc)

    return tree


@router.get("/accounts-page")
def account_page(request: Request, db: Session = Depends(get_db)):

    company_id = get_current_company_id(request)

    accounts = db.query(Account)\
        .filter(Account.company_id == company_id)\
        .all()

    tree_accounts = build_account_tree(accounts)

    return render_template(
        "ProBook/Accounts/accounts.html",  # ✅ fixed
        request,
        {
            "accounts": tree_accounts
        }
    )