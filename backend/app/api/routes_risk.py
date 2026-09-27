from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.db.database import get_db
from app.services.risk_service import RiskService
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/risk", tags=["Risk Intelligence & Mitigations"])

class RiskPredictionRequest(BaseModel):
    latitude: float = Field(..., example=27.5950, description="Target Well Latitude")
    longitude: float = Field(..., example=95.3980, description="Target Well Longitude")
    planned_depth: float = Field(..., example=4000.0, description="Planned Total Depth in meters")
    interval_step_m: float = Field(500.0, description="Depth interval discretization step")
    search_radius_km: float = Field(35.0, description="Offset well search radius in km")
    target_formations: Optional[List[str]] = Field(default=None, description="Optional expected formation names")

@router.post("/predict")
def generate_risk_profile(
    request: RiskPredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Generate depth-wise risk profile, hazard probabilities, and preventive recommendations.
    """
    risk_service = RiskService(db)
    profile = risk_service.generate_depth_risk_profile(
        latitude=request.latitude,
        longitude=request.longitude,
        planned_depth=request.planned_depth,
        interval_step_m=request.interval_step_m,
        search_radius_m=request.search_radius_km * 1000.0
    )
    return profile

@router.get("/recommendations")
def get_preventive_recommendations(
    latitude: float = 27.48,
    longitude: float = 95.35,
    planned_depth: float = 3500.0,
    db: Session = Depends(get_db)
):
    """
    Search historical mitigation actions and preventive practices by event type or depth.
    """
    rec_service = RecommendationService(db)
    return rec_service.generate_recommendations(
        latitude=latitude,
        longitude=longitude,
        planned_depth=planned_depth
    )
