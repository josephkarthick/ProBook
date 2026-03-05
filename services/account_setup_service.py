from models.accounts import Account
from sqlalchemy.orm import Session


def create_default_accounts(db: Session, company_id: int):

    # -------------------------
    # ROOT GROUPS
    # -------------------------
    assets = Account(
        company_id=company_id,
        name="Assets",
        account_type="ASSET",
        is_group=True,
        is_system=True
    )

    liabilities = Account(
        company_id=company_id,
        name="Liabilities",
        account_type="LIABILITY",
        is_group=True,
        is_system=True
    )

    equity = Account(
        company_id=company_id,
        name="Equity",
        account_type="EQUITY",
        is_group=True,
        is_system=True
    )

    income = Account(
        company_id=company_id,
        name="Income",
        account_type="INCOME",
        is_group=True,
        is_system=True
    )

    expense = Account(
        company_id=company_id,
        name="Expense",
        account_type="EXPENSE",
        is_group=True,
        is_system=True
    )

    db.add_all([assets, liabilities, equity, income, expense])
    db.flush()

    # -------------------------
    # SECOND LEVEL GROUPS
    # -------------------------
    current_assets = Account(
        company_id=company_id,
        name="Current Assets",
        account_type="ASSET",
        parent_id=assets.id,
        is_group=True,
        is_system=True
    )

    fixed_assets = Account(
        company_id=company_id,
        name="Fixed Assets",
        account_type="ASSET",
        parent_id=assets.id,
        is_group=True,
        is_system=True
    )

    current_liabilities = Account(
        company_id=company_id,
        name="Current Liabilities",
        account_type="LIABILITY",
        parent_id=liabilities.id,
        is_group=True,
        is_system=True
    )

    direct_income = Account(
        company_id=company_id,
        name="Direct Income",
        account_type="INCOME",
        parent_id=income.id,
        is_group=True,
        is_system=True
    )

    direct_expense = Account(
        company_id=company_id,
        name="Direct Expense",
        account_type="EXPENSE",
        parent_id=expense.id,
        is_group=True,
        is_system=True
    )

    indirect_expense = Account(
        company_id=company_id,
        name="Indirect Expense",
        account_type="EXPENSE",
        parent_id=expense.id,
        is_group=True,
        is_system=True
    )

    db.add_all([
        current_assets,
        fixed_assets,
        current_liabilities,
        direct_income,
        direct_expense,
        indirect_expense
    ])
    db.flush()

    # -------------------------
    # SYSTEM LEDGERS
    # -------------------------
    system_ledgers = [

        # Assets
        Account(company_id=company_id, name="Cash",
                account_type="ASSET",
                parent_id=current_assets.id, is_group=False, is_system=True),

        Account(company_id=company_id, name="Bank",
                account_type="ASSET",
                parent_id=current_assets.id, is_group=False, is_system=True),

        Account(company_id=company_id, name="Accounts Receivable",
                account_type="ASSET",
                parent_id=current_assets.id, is_group=False, is_system=True),

        Account(company_id=company_id, name="Inventory",
                account_type="ASSET",
                parent_id=current_assets.id, is_group=False, is_system=True),

        # Liabilities
        Account(company_id=company_id, name="Accounts Payable",
                account_type="LIABILITY",
                parent_id=current_liabilities.id, is_group=False, is_system=True),

        Account(company_id=company_id, name="GST Payable",
                account_type="LIABILITY",
                parent_id=current_liabilities.id, is_group=False, is_system=True),

        # Income
        Account(company_id=company_id, name="Sales",
                account_type="INCOME",
                parent_id=direct_income.id, is_group=False, is_system=True),

        # Expense
        Account(company_id=company_id, name="Purchase",
                account_type="EXPENSE",
                parent_id=direct_expense.id, is_group=False, is_system=True),

        Account(company_id=company_id, name="Cost of Goods Sold",
                account_type="EXPENSE",
                parent_id=direct_expense.id, is_group=False, is_system=True),

        # Equity
        Account(company_id=company_id, name="Capital",
                account_type="EQUITY",
                parent_id=equity.id, is_group=False, is_system=True),
    ]

    db.add_all(system_ledgers)

    db.commit()