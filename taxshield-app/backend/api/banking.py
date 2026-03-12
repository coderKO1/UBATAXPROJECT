from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.api.deps import get_current_user
from backend.database.session import get_db
from backend.models.entities import Account, Transaction, VATWallet, CITWallet, TaxEstimation
from backend.schemas.dto import TransferRequest, ReceiveRequest, TransactionOut
from backend.tax_engine.engine import NARRATION_TO_TYPE, handle_tax_for_transaction, compute_metrics

router = APIRouter(prefix="/banking", tags=["banking"])


@router.get("/dashboard")
def dashboard(user=Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.user_id == user.id).first()
    metrics = compute_metrics(db, account.id)
    recent = (
        db.query(Transaction)
        .filter(Transaction.account_id == account.id)
        .order_by(desc(Transaction.date))
        .limit(8)
        .all()
    )
    return {
        "account_balance": account.balance,
        "recent_transactions": [TransactionOut.model_validate(tx).model_dump() for tx in recent],
        "monthly_income": metrics["inflow"],
        "monthly_expenses": metrics["outflow"],
        "profit": metrics["profit"],
        "estimated_annual_tax": metrics["estimated_tax"],
        "vat_wallet": metrics["vat_wallet"],
        "cit_wallet": metrics["cit_wallet"],
    }


@router.get("/transactions", response_model=list[TransactionOut])
def transactions(user=Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.user_id == user.id).first()
    return db.query(Transaction).filter(Transaction.account_id == account.id).order_by(desc(Transaction.date)).all()


@router.post("/transfer")
def transfer(payload: TransferRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if payload.category not in NARRATION_TO_TYPE:
        raise HTTPException(status_code=400, detail="Invalid narration category")

    account = db.query(Account).filter(Account.user_id == user.id).first()
    if account.balance < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    tx_type = NARRATION_TO_TYPE[payload.category]
    account.balance -= payload.amount
    tx = Transaction(
        account_id=account.id,
        amount=payload.amount,
        type=tx_type,
        category=payload.category,
        description=payload.description,
        sender=user.name,
        receiver=payload.receiver,
    )
    db.add(tx)
    db.commit()
    handle_tax_for_transaction(db, account.id, payload.amount, tx_type)
    return {"status": "success"}


@router.post("/receive")
def receive(payload: ReceiveRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.user_id == user.id).first()
    tx_type = NARRATION_TO_TYPE.get(payload.category, "INFLOW")
    account.balance += payload.amount
    tx = Transaction(
        account_id=account.id,
        amount=payload.amount,
        type=tx_type,
        category=payload.category,
        description=payload.description,
        sender=payload.sender,
        receiver=user.name,
    )
    db.add(tx)
    db.commit()
    handle_tax_for_transaction(db, account.id, payload.amount, tx_type)
    return {"status": "success"}


@router.get("/wallets")
def wallets(user=Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.user_id == user.id).first()
    vat = db.query(VATWallet).filter(VATWallet.account_id == account.id).first()
    cit = db.query(CITWallet).filter(CITWallet.account_id == account.id).first()
    est = db.query(TaxEstimation).filter(TaxEstimation.account_id == account.id).first()
    return {
        "vat_wallet": vat.balance if vat else 0,
        "cit_wallet": cit.balance if cit else 0,
        "estimated": est.estimated_tax if est else 0,
        "formulas": {
            "profit": "Income - Expenses",
            "cit": "Profit × 30%",
            "vat": "7.5% of inflow transactions after annual turnover > 100,000,000",
        },
    }
