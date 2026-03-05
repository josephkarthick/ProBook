from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal

from models.accounts import Account
from models.journal_line import JournalLine
from models.journal_entry import JournalEntry

from schemas.profit_loss_schema import ProfitLossRow, ProfitLossResponse


def get_profit_loss(db: Session, company_id: int):

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

    income_rows = []
    expense_rows = []

    total_income = Decimal("0")
    total_expense = Decimal("0")

    for r in rows:

        if r.account_type == "INCOME":

            amount = r.credit - r.debit
            total_income += amount

            income_rows.append(
                ProfitLossRow(
                    account_id=r.id,
                    account_name=r.name,
                    amount=amount
                )
            )

        elif r.account_type == "EXPENSE":

            amount = r.debit - r.credit
            total_expense += amount

            expense_rows.append(
                ProfitLossRow(
                    account_id=r.id,
                    account_name=r.name,
                    amount=amount
                )
            )

    net_profit = total_income - total_expense

    return ProfitLossResponse(
        income=income_rows,
        expense=expense_rows,
        total_income=total_income,
        total_expense=total_expense,
        net_profit=net_profit
    )