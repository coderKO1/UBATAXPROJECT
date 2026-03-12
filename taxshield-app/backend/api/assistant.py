from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.deps import get_current_user
from backend.database.session import get_db
from backend.models.entities import Account
from backend.schemas.dto import AIQueryRequest
from backend.ai.assistant import financial_query_engine

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/query")
def ask(payload: AIQueryRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.user_id == user.id).first()
    answer = financial_query_engine(db, account.id, payload.question)
    return {"answer": answer}
