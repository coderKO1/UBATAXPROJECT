from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.session import get_db
from backend.models.entities import User, Account, VATWallet, CITWallet
from backend.schemas.dto import LoginRequest, RegisterRequest, TokenResponse
from backend.services.security import verify_password, hash_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already in use")

    user = User(name=payload.name, email=payload.email, password=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    account = Account(user_id=user.id, balance=2500000)
    db.add(account)
    db.commit()
    db.refresh(account)

    db.add(VATWallet(account_id=account.id, balance=0))
    db.add(CITWallet(account_id=account.id, balance=0))
    db.commit()

    return TokenResponse(access_token=create_access_token(user.email))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(user.email))
