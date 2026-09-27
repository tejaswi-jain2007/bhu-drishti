from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.db.models.base import get_db
from app.services.rag_service import RAGService

router = APIRouter()

class AssistantQuery(BaseModel):
    question: Optional[str] = None
    query: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius: float = 50000.0

@router.post("/query")
async def query_assistant(
    query_req: AssistantQuery,
    db: Session = Depends(get_db)
):
    """Query the Drilling AI Assistant with natural language question (FR-19)"""
    user_prompt = query_req.question or query_req.query
    if not user_prompt:
        raise HTTPException(status_code=400, detail="Either 'question' or 'query' must be provided.")

    radius_m = query_req.radius * 1000.0 if query_req.radius <= 500.0 else query_req.radius

    try:
        rag_service = RAGService(db)
        result = rag_service.answer_question(
            question=user_prompt,
            latitude=query_req.latitude,
            longitude=query_req.longitude,
            radius=radius_m
        )
        return {
            "answer": result["answer"],
            "citations": result.get("citations", []),
            "intent": result.get("intent", "general"),
            "confidence": result.get("confidence", 0.90)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
