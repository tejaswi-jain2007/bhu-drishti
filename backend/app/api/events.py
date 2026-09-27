from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.db.models.base import get_db
from app.db.models.event import Event, Mitigation

router = APIRouter()

class EventResponse(BaseModel):
    event_id: int
    well_id: int
    event_type: str
    start_depth: float
    end_depth: Optional[float]
    severity: Optional[str]
    description: Optional[str]
    npt_hours: Optional[float]
    mitigation_successful: bool
    source: str
    confidence: float
    mitigations: List[dict]

@router.get("/wells/{well_id}", response_model=List[EventResponse])
async def get_well_events(well_id: int, db: Session = Depends(get_db)):
    """Get historical events for a specific well"""
    events = db.query(Event).filter(Event.well_id == well_id).order_by(Event.start_depth).all()
    
    if not events:
        raise HTTPException(status_code=404, detail="No events found for this well")
    
    event_responses = []
    for event in events:
        mitigations = db.query(Mitigation).filter(Mitigation.event_id == event.event_id).all()
        
        event_responses.append(EventResponse(
            event_id=event.event_id,
            well_id=event.well_id,
            event_type=event.event_type,
            start_depth=event.start_depth,
            end_depth=event.end_depth,
            severity=event.severity,
            description=event.description,
            npt_hours=event.npt_hours,
            mitigation_successful=event.mitigation_successful,
            source=event.source,
            confidence=event.confidence,
            mitigations=[
                {
                    "action": m.action,
                    "outcome": m.outcome,
                    "source_document": m.source_document,
                    "confidence": m.confidence
                }
                for m in mitigations
            ]
        ))
    
    return event_responses
