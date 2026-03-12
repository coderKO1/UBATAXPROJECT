from datetime import datetime
from sqlalchemy import extract, func
from sqlalchemy.orm import Session
from backend.models.entities import Transaction, VATWallet, CITWallet, TaxEstimation

VAT_THRESHOLD = 100_000_000
VAT_RATE = 0.075
CIT_RATE = 0.30


NARRATION_TO_TYPE = {
    "Business Expense": "OUTFLOW",
    "Inventory Purchase": "OUTFLOW",
    "Salary Payment": "OUTFLOW",
    "Operational Expense": "OUTFLOW",
    "Customer Payment": "INFLOW",
    "Personal Transfer": "OUTFLOW",
    "Investment": "INFLOW",
    "Loan Repayment": "OUTFLOW",
}


def compute_metrics(db: Session, account_id: int):
    txs = db.query(Transaction).filter(Transaction.account_id == account_id).all()
    inflow = sum(t.amount for t in txs if t.type == "INFLOW")
    outflow = sum(t.amount for t in txs if t.type == "OUTFLOW")
    profit = inflow - outflow

    current_year = datetime.utcnow().year
    monthly_income = (
        db.query(extract("month", Transaction.date).label("month"), func.sum(Transaction.amount))
        .filter(Transaction.account_id == account_id, Transaction.type == "INFLOW", extract("year", Transaction.date) == current_year)
        .group_by("month")
        .all()
    )
    avg_monthly = (sum(row[1] for row in monthly_income) / len(monthly_income)) if monthly_income else 0
    estimated_annual_income = avg_monthly * 12

    vat_wallet = db.query(VATWallet).filter(VATWallet.account_id == account_id).first()
    cit_wallet = db.query(CITWallet).filter(CITWallet.account_id == account_id).first()
    if not vat_wallet:
        vat_wallet = VATWallet(account_id=account_id, balance=0)
        db.add(vat_wallet)
    if not cit_wallet:
        cit_wallet = CITWallet(account_id=account_id, balance=0)
        db.add(cit_wallet)

    estimated_tax = 0
    if estimated_annual_income > VAT_THRESHOLD:
        estimated_tax = max(profit, 0) * CIT_RATE

    estimation = db.query(TaxEstimation).filter(TaxEstimation.account_id == account_id).first()
    if not estimation:
        estimation = TaxEstimation(account_id=account_id)
        db.add(estimation)
    estimation.estimated_annual_income = estimated_annual_income
    estimation.estimated_profit = profit
    estimation.estimated_tax = estimated_tax
    estimation.updated_at = datetime.utcnow()
    db.commit()

    return {
        "inflow": inflow,
        "outflow": outflow,
        "profit": profit,
        "estimated_annual_income": estimated_annual_income,
        "estimated_tax": estimated_tax,
        "vat_wallet": vat_wallet.balance,
        "cit_wallet": cit_wallet.balance,
    }


def handle_tax_for_transaction(db: Session, account_id: int, amount: float, tx_type: str):
    stats = compute_metrics(db, account_id)
    annual_income = stats["estimated_annual_income"]
    if annual_income <= VAT_THRESHOLD:
        return

    vat_wallet = db.query(VATWallet).filter(VATWallet.account_id == account_id).first()
    cit_wallet = db.query(CITWallet).filter(CITWallet.account_id == account_id).first()

    if tx_type == "INFLOW":
        vat_wallet.balance += amount * VAT_RATE

    if stats["profit"] > 0:
        cit_wallet.balance = stats["profit"] * CIT_RATE

    db.commit()
