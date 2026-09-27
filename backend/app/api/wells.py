from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel
from app.db.database import get_db
from app.db.models import Well, WellTrajectory, Formation, DrillingEvent
from app.services.spatial_service import SpatialService
from app.services.correlation_service import CorrelationService
from app.db.seed_pan_india import DISTRICT_CENTERS
import uuid

router = APIRouter()

class WellPlanCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    planned_depth: float
    state: Optional[str] = None
    district: Optional[str] = None
    geological_info: Optional[str] = None
    search_radius: float = 50000  # meters

class WellPlanResponse(BaseModel):
    plan_id: str
    name: str
    latitude: float
    longitude: float
    planned_depth: float
    state: Optional[str]
    district: Optional[str]
    geological_info: Optional[str]
    search_radius: float

class NearbyWellResponse(BaseModel):
    well_id: Union[str, int]
    name: str
    operator: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    state: Optional[str] = None
    district: Optional[str] = None
    well_type: Optional[str] = None
    distance: float
    bearing: Optional[float] = 0.0
    direction: Optional[str] = "N"
    total_depth: Optional[float] = None
    spud_year: Optional[int] = None
    field: Optional[str] = None
    block: Optional[str] = None
    historical_events_count: Optional[int] = 0

class CorrelationRequest(BaseModel):
    latitude: float
    longitude: float
    planned_depth: float
    search_radius: float = 50000.0
    limit_wells: int = 5

@router.get("/districts")
async def get_states_and_districts():
    """Retrieve supported Indian petroleum exploration states and district centers (FR-01)"""
    return {
        "states": list(DISTRICT_CENTERS.keys()),
        "districts_by_state": {
            state: [
                {"district": d_name, "latitude": coords[0], "longitude": coords[1]}
                for d_name, coords in districts.items()
            ]
            for state, districts in DISTRICT_CENTERS.items()
        }
    }

@router.get("/locations")
async def get_locations(db: Session = Depends(get_db)):
    """Get distinct states and districts"""
    return SpatialService.get_distinct_locations(db)

@router.post("/plans", response_model=WellPlanResponse)
async def create_well_plan(plan: WellPlanCreate, db: Session = Depends(get_db)):
    """Create a proposed well plan for analysis"""
    plan_id = str(uuid.uuid4())
    return WellPlanResponse(
        plan_id=plan_id,
        name=plan.name,
        latitude=plan.latitude,
        longitude=plan.longitude,
        planned_depth=plan.planned_depth,
        state=plan.state,
        district=plan.district,
        geological_info=plan.geological_info,
        search_radius=plan.search_radius
    )

@router.get("/nearby", response_model=List[NearbyWellResponse])
async def get_nearby_wells(
    lat: Optional[float] = Query(None, description="Latitude of proposed location"),
    lon: Optional[float] = Query(None, description="Longitude of proposed location"),
    latitude: Optional[float] = Query(None, description="Alias for lat"),
    longitude: Optional[float] = Query(None, description="Alias for lon"),
    radius: Optional[float] = Query(None, description="Search radius in meters or km"),
    radius_km: Optional[float] = Query(None, description="Search radius in km"),
    db: Session = Depends(get_db)
):
    """Find historical wells within a specified radius (FR-05)"""
    target_lat = lat if lat is not None else latitude
    target_lon = lon if lon is not None else longitude
    
    if target_lat is None or target_lon is None:
        raise HTTPException(status_code=400, detail="Latitude and longitude coordinates are required.")

    target_radius = 50000.0
    if radius_km is not None:
        target_radius = radius_km * 1000.0
    elif radius is not None:
        target_radius = radius * 1000.0 if radius <= 500 else radius

    spatial_service = SpatialService(db)
    nearby_wells = spatial_service.find_nearby_wells(target_lat, target_lon, target_radius)
    return nearby_wells

@router.post("/correlation")
async def get_cross_well_correlation(
    req: CorrelationRequest,
    db: Session = Depends(get_db)
):
    """Correlate offset wells stratigraphy and events against target depth (FR-09)"""
    corr_service = CorrelationService(db)
    radius_m = req.search_radius * 1000.0 if req.search_radius <= 500 else req.search_radius
    return corr_service.get_cross_well_correlation(
        latitude=req.latitude,
        longitude=req.longitude,
        planned_depth=req.planned_depth,
        radius=radius_m,
        limit_wells=req.limit_wells
    )

@router.get("/hydrocarbon-evidence")
async def get_hydrocarbon_evidence_get(
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    radius_km: Optional[float] = Query(50.0),
    db: Session = Depends(get_db)
):
    """Retrieve historical hydrocarbon evidence (oil/gas shows, DST tests) from offset wells"""
    from app.services.risk_service import RiskService
    t_lat = lat if lat is not None else (latitude or 27.6015)
    t_lon = lon if lon is not None else (longitude or 95.4051)
    risk_service = RiskService(db)
    return risk_service.get_hydrocarbon_evidence(
        target_lat=t_lat,
        target_lon=t_lon,
        radius_m=(radius_km or 50.0) * 1000.0
    )

@router.get("/{well_id}")
async def get_well_profile(well_id: str, db: Session = Depends(get_db)):
    """Get detailed well profile including trajectory, formations, and documents (FR-06)"""
    well = db.query(Well).filter(Well.well_id == str(well_id)).first()
    if not well:
        raise HTTPException(status_code=404, detail="Well not found")

    trajectory = [
        {
            "md": t.md,
            "tvd": t.tvd,
            "tvdss": getattr(t, "tvdss", t.tvd),
            "inclination": getattr(t, "inclination", 0.0),
            "azimuth": getattr(t, "azimuth", 0.0),
            "dogleg_severity": getattr(t, "dogleg_severity", 0.0)
        }
        for t in (well.trajectories if hasattr(well, 'trajectories') else [])
    ]

    formations = [
        {
            "formation_name": f.formation_name,
            "top_depth": f.top_depth_md,
            "base_depth": f.base_depth_md,
            "lithology": f.lithology,
            "age": getattr(f, "age", "Tertiary"),
            "description": getattr(f, "description", "")
        }
        for f in (well.formations if hasattr(well, 'formations') else [])
    ]

    return {
        "well_id": well.well_id,
        "name": well.name,
        "operator": getattr(well, "operator", "Oil India Limited"),
        "latitude": well.latitude,
        "longitude": well.longitude,
        "spud_date": well.spud_date.isoformat() if well.spud_date else None,
        "completion_date": well.completion_date.isoformat() if well.completion_date else None,
        "total_depth": well.total_depth,
        "well_type": getattr(well, "well_type", "Exploratory"),
        "field": getattr(well, "field", "Upper Assam"),
        "block": getattr(well, "block", None),
        "state": getattr(well, "state", "Assam"),
        "district": getattr(well, "district", "Dibrugarh"),
        "trajectory": trajectory,
        "formations": formations,
        "documents": []
    }

@router.get("/{well_id}/events")
async def get_well_events(well_id: str, db: Session = Depends(get_db)):
    """Get historical drilling events with evidence and mitigations (FR-08)"""
    events = db.query(DrillingEvent).filter(DrillingEvent.well_id == str(well_id)).order_by(DrillingEvent.start_depth_md).all()
    results = []

    for ev in events:
        mitigations_list = [
            {
                "action": m.action_taken,
                "outcome": m.outcome,
                "source_document": m.source_reference,
                "confidence": 0.95
            }
            for m in (ev.mitigations if hasattr(ev, 'mitigations') else [])
        ]

        results.append({
            "event_id": ev.event_id,
            "event_type": ev.event_type,
            "start_depth": ev.start_depth_md,
            "end_depth": ev.end_depth_md,
            "severity": ev.severity,
            "description": ev.description,
            "npt_hours": getattr(ev, "npt_hours", 0.0),
            "mitigation_successful": True,
            "source": getattr(ev, "source_document", "WCR/DDR"),
            "confidence": getattr(ev, "extraction_confidence", 0.95),
            "evidence": [
                {
                    "page_number": getattr(ev, "page_number", 1),
                    "evidence_text": getattr(ev, "evidence_text", ev.description),
                    "extraction_method": "NLP/OCR",
                    "confidence": getattr(ev, "extraction_confidence", 0.95)
                }
            ],
            "mitigations": mitigations_list
        })

    return results
