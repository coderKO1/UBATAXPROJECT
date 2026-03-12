from datetime import date
from sqlalchemy.orm import Session
from backend.models.entities import Employee, PayrollRecord, Account, Transaction
from backend.tax_engine.engine import NARRATION_TO_TYPE


def calculate_annual_paye(taxable_income: float) -> float:
    if taxable_income <= 800_000:
        return 0
    excess = taxable_income - 800_000
    return excess * 0.2


def add_employee(db: Session, account_id: int, name: str, salary: float, pension: float, nhis: float):
    employee = Employee(business_id=account_id, name=name, salary=salary, pension=pension, nhis=nhis)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def validate_salary(db: Session, account_id: int):
    account = db.query(Account).filter(Account.id == account_id).first()
    employees = db.query(Employee).filter(Employee.business_id == account_id).all()
    records = []

    for emp in employees:
        taxable = max(emp.salary - emp.pension - emp.nhis, 0)
        annual_tax = calculate_annual_paye(taxable * 12)
        monthly_paye = annual_tax / 12
        net = emp.salary - monthly_paye

        account.balance -= emp.salary
        tx = Transaction(
            account_id=account_id,
            amount=emp.salary,
            type=NARRATION_TO_TYPE["Salary Payment"],
            category="Salary Payment",
            description=f"Salary paid to {emp.name}",
            sender="Business Account",
            receiver=emp.name,
        )
        db.add(tx)

        record = PayrollRecord(
            employee_id=emp.id,
            gross_salary=emp.salary,
            taxable_income=taxable,
            paye_deduction=monthly_paye,
            date=date.today(),
        )
        db.add(record)
        records.append({"employee": emp.name, "gross": emp.salary, "paye": monthly_paye, "net": net})

    db.commit()
    return records
