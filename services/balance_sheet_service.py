from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal

from models.accounts import Account
from models.journal_line import JournalLine
from models.journal_entry import JournalEntry

from schemas.balance_sheet_schema import BalanceSheetRow, BalanceSheetResponse


def get_balance_sheet(db: Session, company_id: int):

    rows = db.query(

        Account.id,
        Account.name,
        Account.account_type,

        func.coalesce(func.sum(JournalLine.debit),0).label("debit"),
        func.coalesce(func.sum(JournalLine.credit),0).label("credit")

    ).join(JournalLine, JournalLine.account_id == Account.id)\
     .join(JournalEntry, JournalEntry.id == JournalLine.journal_id)\
     .filter(JournalEntry.company_id == company_id)\
     .group_by(Account.id, Account.name, Account.account_type)\
     .all()

    assets = []
    liabilities = []
    equity = []

    total_assets = Decimal("0")
    total_liabilities = Decimal("0")
    total_equity = Decimal("0")

    for r in rows:

        if r.account_type == "ASSET":

            amount = r.debit - r.credit
            total_assets += amount

            assets.append(
                BalanceSheetRow(
                    account_id=r.id,
                    account_name=r.name,
                    amount=amount
                )
            )

        elif r.account_type == "LIABILITY":

            amount = r.credit - r.debit
            total_liabilities += amount

            liabilities.append(
                BalanceSheetRow(
                    account_id=r.id,
                    account_name=r.name,
                    amount=amount
                )
            )

        elif r.account_type == "EQUITY":

            amount = r.credit - r.debit
            total_equity += amount

            equity.append(
                BalanceSheetRow(
                    account_id=r.id,
                    account_name=r.name,
                    amount=amount
                )
            )

    return BalanceSheetResponse(
        assets=assets,
        liabilities=liabilities,
        equity=equity,
        total_assets=total_assets,
        total_liabilities=total_liabilities,
        total_equity=total_equity
    )