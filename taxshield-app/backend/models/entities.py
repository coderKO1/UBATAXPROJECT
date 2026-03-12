from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from backend.database.session import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("Account", back_populates="user", uselist=False)


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="account")
    transactions = relationship("Transaction", back_populates="account")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    sender = Column(String, nullable=False)
    receiver = Column(String, nullable=False)

    account = relationship("Account", back_populates="transactions")


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    name = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    pension = Column(Float, nullable=False)
    nhis = Column(Float, nullable=False)


class PayrollRecord(Base):
    __tablename__ = "payroll_records"
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    gross_salary = Column(Float, nullable=False)
    taxable_income = Column(Float, nullable=False)
    paye_deduction = Column(Float, nullable=False)
    date = Column(Date, default=date.today)


class VATWallet(Base):
    __tablename__ = "vat_wallet"
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    balance = Column(Float, default=0)


class CITWallet(Base):
    __tablename__ = "cit_wallet"
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    balance = Column(Float, default=0)


class TaxEstimation(Base):
    __tablename__ = "tax_estimations"
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    estimated_annual_income = Column(Float, default=0)
    estimated_profit = Column(Float, default=0)
    estimated_tax = Column(Float, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)
