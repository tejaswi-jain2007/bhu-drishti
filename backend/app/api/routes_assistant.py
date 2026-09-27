from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.db.database import get_db
from app.services.rag_service import DrillingRAGAssistant

router = APIRouter(prefix="/assistant", tags=["AI Drilling Assistant (RAG)"])

class QueryRequest(BaseModel):
    query: str = Field(..., example="Show nearby wells that experienced mud loss around 2800 m.")

@router.post("/query")
def query_assistant(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """
    Natural-language QA with zero-hallucination source provenance citations.
    """
    return DrillingRAGAssistant.answer_query(db=db, user_query=request.query)
