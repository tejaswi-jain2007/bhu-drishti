from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.db.models.base import get_db
from app.services.recommendation_service import RecommendationService

router = APIRouter()

class RecommendationRequest(BaseModel):
    latitude: float
    longitude: float
    planned_depth: float
    geological_formation: Optional[str] = ""
    search_radius: float = 50000.0
    search_radius_km: Optional[float] = None

@router.post("")
async def get_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """Generate engineering preventive recommendations based on offset wells (FR-16)"""
    radius_m = 50000.0
    if request.search_radius_km is not None:
        radius_m = request.search_radius_km * 1000.0
    elif request.search_radius <= 500.0:
        radius_m = request.search_radius * 1000.0
    else:
        radius_m = request.search_radius

    rec_service = RecommendationService(db)
    return rec_service.generate_recommendations(
        latitude=request.latitude,
        longitude=request.longitude,
        planned_depth=request.planned_depth,
        geological_formation=request.geological_formation or "",
        search_radius_m=radius_m
    )
