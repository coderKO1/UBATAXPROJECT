from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.database.session import Base, engine, SessionLocal
from backend.models.entities import User, Account, Transaction, Employee, VATWallet, CITWallet
from backend.services.security import hash_password
from backend.api import auth, banking, payroll, analytics, assistant

app = FastAPI(title="TaxShield API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(banking.router, prefix="/api")
app.include_router(payroll.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(assistant.router, prefix="/api")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    seed_data()


def seed_data():
    db: Session = SessionLocal()
    try:
        if db.query(User).count() > 0:
            return

        user = User(name="TaxShield Demo SME", email="demo@taxshield.com", password=hash_password("password123"))
        db.add(user)
        db.commit()
        db.refresh(user)

        account = Account(user_id=user.id, balance=12000000)
        db.add(account)
        db.commit()
        db.refresh(account)

        db.add(VATWallet(account_id=account.id, balance=0))
        db.add(CITWallet(account_id=account.id, balance=0))

        samples = [
            Transaction(account_id=account.id, amount=5000000, type="INFLOW", category="Customer Payment", description="Invoice payment", sender="Zenith Retail", receiver=user.name),
            Transaction(account_id=account.id, amount=2000000, type="OUTFLOW", category="Inventory Purchase", description="Stock replenishment", sender=user.name, receiver="ABC Supplies"),
            Transaction(account_id=account.id, amount=4000000, type="INFLOW", category="Investment", description="Seed extension", sender="Investor Group", receiver=user.name),
            Transaction(account_id=account.id, amount=800000, type="OUTFLOW", category="Operational Expense", description="Internet and utility", sender=user.name, receiver="Service Providers"),
        ]
        db.add_all(samples)

        employees = [
            Employee(business_id=account.id, name="Ada Okafor", salary=350000, pension=28000, nhis=10000),
            Employee(business_id=account.id, name="Emeka Bello", salary=420000, pension=33600, nhis=10000),
        ]
        db.add_all(employees)
        db.commit()
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}
