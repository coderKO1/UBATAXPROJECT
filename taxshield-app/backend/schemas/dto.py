from datetime import datetime
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(LoginRequest):
    name: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TransferRequest(BaseModel):
    amount: float
    receiver: str
    category: str
    description: str


class ReceiveRequest(BaseModel):
    amount: float
    sender: str
    category: str = "Customer Payment"
    description: str = "Payment received"


class EmployeeRequest(BaseModel):
    name: str
    salary: float
    pension: float
    nhis: float


class AIQueryRequest(BaseModel):
    question: str


class TransactionOut(BaseModel):
    id: int
    amount: float
    date: datetime
    type: str
    sender: str
    receiver: str
    category: str
    description: str

    class Config:
        from_attributes = True
