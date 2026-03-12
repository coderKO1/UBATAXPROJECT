from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.api.deps import get_current_user
from backend.database.session import get_db
from backend.models.entities import Account, Transaction, PayrollRecord
from backend.tax_engine.engine import compute_metrics

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("")
def analytics(user=Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.user_id == user.id).first()
    metrics = compute_metrics(db, account.id)

    daily = (
        db.query(func.date(Transaction.date), func.sum(Transaction.amount))
        .filter(Transaction.account_id == account.id)
        .group_by(func.date(Transaction.date))
        .all()
    )
    monthly_income = (
        db.query(func.date_part("month", Transaction.date), func.sum(Transaction.amount))
        .filter(Transaction.account_id == account.id, Transaction.type == "INFLOW")
        .group_by(func.date_part("month", Transaction.date))
        .all()
    )
    expenses = (
        db.query(Transaction.category, func.sum(Transaction.amount))
        .filter(Transaction.account_id == account.id, Transaction.type == "OUTFLOW")
        .group_by(Transaction.category)
        .all()
    )
    payroll_cost = db.query(func.sum(PayrollRecord.gross_salary)).scalar() or 0

    return {
        "daily_transactions": [{"date": str(d), "amount": a} for d, a in daily],
        "monthly_income": [{"month": int(m), "amount": a} for m, a in monthly_income],
        "expenses_breakdown": [{"category": c, "amount": a} for c, a in expenses],
        "profit": metrics["profit"],
        "estimated_tax": metrics["estimated_tax"],
        "vat_wallet": metrics["vat_wallet"],
        "cit_wallet": metrics["cit_wallet"],
        "payroll_costs": payroll_cost,
    }
