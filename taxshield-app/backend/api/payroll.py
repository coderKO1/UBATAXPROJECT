from datetime import date, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.deps import get_current_user
from backend.database.session import get_db
from backend.models.entities import Account, Employee, PayrollRecord
from backend.schemas.dto import EmployeeRequest
from backend.payroll.engine import add_employee, validate_salary

router = APIRouter(prefix="/payroll", tags=["payroll"])


@router.post("/employees")
def create_employee(payload: EmployeeRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.user_id == user.id).first()
    employee = add_employee(db, account.id, payload.name, payload.salary, payload.pension, payload.nhis)
    return {"id": employee.id, "name": employee.name}


@router.get("/employees")
def list_employees(user=Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.user_id == user.id).first()
    employees = db.query(Employee).filter(Employee.business_id == account.id).all()
    return [
        {"id": e.id, "name": e.name, "salary": e.salary, "pension": e.pension, "nhis": e.nhis}
        for e in employees
    ]


@router.post("/validate-salary")
def execute_payroll(user=Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.user_id == user.id).first()
    records = validate_salary(db, account.id)
    return {"status": "processed", "records": records}


@router.get("/reminders")
def reminders():
    today = date.today()
    pay_day = date(today.year, today.month, 28)
    delta = (pay_day - today).days
    reminders = []
    for d in [7, 2, 1]:
        if delta == d:
            reminders.append(f"Salary due in {d} day(s)")
    return {"days_to_salary": delta, "alerts": reminders}
