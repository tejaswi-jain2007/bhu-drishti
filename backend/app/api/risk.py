from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.db.models.base import get_db
from app.services.risk_service import RiskService

router = APIRouter()

class RiskAnalysisRequest(BaseModel):
    plan_id: Optional[str] = None
    latitude: float
    longitude: float
    planned_depth: float
    search_radius: float = 50000.0  # meters
    search_radius_km: Optional[float] = None
    interval_step_m: float = 500.0

class CandidateLocationRequest(BaseModel):
    latitude: float
    longitude: float
    planned_depth: float
    search_radius: float = 50000.0
    search_radius_km: Optional[float] = None

class HydrocarbonEvidenceRequest(BaseModel):
    latitude: float
    longitude: float
    search_radius: float = 50000.0
    search_radius_km: Optional[float] = None

@router.post("/analyze")
async def analyze_well_risk(
    request: RiskAnalysisRequest,
    db: Session = Depends(get_db)
):
    """Generate depth-wise risk profile based on nearby offset wells (FR-10, FR-11)"""
    radius_m = 50000.0
    if request.search_radius_km is not None:
        radius_m = request.search_radius_km * 1000.0
    elif request.search_radius <= 500.0:
        radius_m = request.search_radius * 1000.0
    else:
        radius_m = request.search_radius

    risk_service = RiskService(db)
    profile = risk_service.generate_depth_risk_profile(
        latitude=request.latitude,
        longitude=request.longitude,
        planned_depth=request.planned_depth,
        interval_step_m=request.interval_step_m,
        search_radius_m=radius_m
    )
    return {
        "plan_id": request.plan_id or "auto-plan",
        "risk_profile": profile
    }

@router.post("/candidates")
async def compare_candidate_locations(
    request: CandidateLocationRequest,
    db: Session = Depends(get_db)
):
    """Evaluate candidate drilling locations to suggest lower-risk alternatives (FR-14)"""
    risk_service = RiskService(db)
    candidates = risk_service.compare_candidate_locations(
        base_lat=request.latitude,
        base_lon=request.longitude,
        planned_depth=request.planned_depth,
        radius_m=request.search_radius
    )
    return {
        "base_location": {"latitude": request.latitude, "longitude": request.longitude},
        "candidate_locations": candidates
    }

@router.post("/hydrocarbon-evidence")
async def get_hydrocarbon_evidence(
    request: HydrocarbonEvidenceRequest,
    db: Session = Depends(get_db)
):
    """Retrieve historical hydrocarbon evidence (oil/gas shows, DST tests) from offset wells (FR-15)"""
    risk_service = RiskService(db)
    return risk_service.get_hydrocarbon_evidence(
        target_lat=request.latitude,
        target_lon=request.longitude,
        radius_m=request.search_radius
    )
