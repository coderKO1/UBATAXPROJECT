import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from openai import OpenAI
from backend.models.entities import Transaction, TaxEstimation


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None


def financial_query_engine(db: Session, account_id: int, question: str):
    q = question.lower()
    now = datetime.utcnow()

    if "last week" in q and "transfer" in q:
        start = now - timedelta(days=7)
        total = (
            db.query(func.sum(Transaction.amount))
            .filter(Transaction.account_id == account_id, Transaction.type == "OUTFLOW", Transaction.date >= start)
            .scalar()
            or 0
        )
        return f"You transferred ₦{total:,.2f} in the last week."

    if "spent this month" in q:
        total = (
            db.query(func.sum(Transaction.amount))
            .filter(
                Transaction.account_id == account_id,
                Transaction.type == "OUTFLOW",
                func.date_part("month", Transaction.date) == now.month,
                func.date_part("year", Transaction.date) == now.year,
            )
            .scalar()
            or 0
        )
        return f"Your total expenses this month are ₦{total:,.2f}."

    if "estimated tax" in q:
        est = db.query(TaxEstimation).filter(TaxEstimation.account_id == account_id).first()
        tax = est.estimated_tax if est else 0
        return f"Estimated annual tax is currently ₦{tax:,.2f}."

    if "patronized" in q or "customer" in q:
        row = (
            db.query(Transaction.sender, func.sum(Transaction.amount).label("total"))
            .filter(Transaction.account_id == account_id, Transaction.type == "INFLOW")
            .group_by(Transaction.sender)
            .order_by(func.sum(Transaction.amount).desc())
            .first()
        )
        if row:
            return f"{row[0]} has patronized you the most with ₦{row[1]:,.2f}."
        return "No inflow records yet."

    if client:
        prompt = "You are TaxShield AI for Nigerian SME tax and finance guidance. Keep responses concise."
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}, {"role": "user", "content": question}],
        )
        return completion.choices[0].message.content

    return "I can explain VAT, CIT, PAYE, deductions, and account spending trends."
