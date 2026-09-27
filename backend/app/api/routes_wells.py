from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.db.models import Well, DrillingEvent, Formation, WellTrajectory
from app.services.spatial_service import SpatialService

router = APIRouter(prefix="/wells", tags=["Wells & Spatial Discovery"])

@router.get("/locations")
def get_available_locations(db: Session = Depends(get_db)):
    """
    Get available states and districts in the institutional database.
    """
    return SpatialService.get_distinct_locations(db)

@router.get("/provinces")
def get_provinces(db: Session = Depends(get_db)):
    """
    Get available provinces/states in the database.
    """
    return SpatialService.get_distinct_locations(db)

@router.get("/nearby")
def get_nearby_wells(
    latitude: float = Query(..., description="Target Latitude (e.g., 27.5921 for Assam)"),
    longitude: float = Query(..., description="Target Longitude (e.g., 95.3942)"),
    radius_km: float = Query(25.0, description="Search radius in kilometers"),
    state: Optional[str] = Query(None, description="Filter by State"),
    district: Optional[str] = Query(None, description="Filter by District"),
    db: Session = Depends(get_db)
):
    """
    Search and retrieve historical offset wells within a given radius.
    """
    results = SpatialService.get_nearby_wells(
        db=db,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        state=state,
        district=district
    )
    return {
        "target_coordinates": {"latitude": latitude, "longitude": longitude},
        "search_radius_km": radius_km,
        "wells_found_count": len(results),
        "wells": results
    }

@router.get("/{well_id}")
def get_well_profile(well_id: str, db: Session = Depends(get_db)):
    """
    Get comprehensive well profile including metadata, formations, trajectory, and historical incidents.
    """
    well = db.query(Well).filter(Well.well_id == well_id).first()
    if not well:
        raise HTTPException(status_code=404, detail=f"Well {well_id} not found.")

    formations = [
        {
            "formation_name": f.formation_name,
            "top_depth_md": f.top_depth_md,
            "base_depth_md": f.base_depth_md,
            "lithology": f.lithology,
            "porosity_avg": f.porosity_avg,
            "permeability_avg": f.permeability_avg,
            "description": f.description
        }
        for f in well.formations
    ]

    events = [
        {
            "event_id": e.event_id,
            "event_type": e.event_type,
            "start_depth_md": e.start_depth_md,
            "end_depth_md": e.end_depth_md,
            "formation_name": e.formation_name,
            "severity": e.severity,
            "npt_hours": e.npt_hours,
            "description": e.description,
            "root_cause": e.root_cause,
            "source_document": e.source_document,
            "page_number": e.page_number,
            "extraction_confidence": e.extraction_confidence,
            "mitigations": [
                {
                    "mitigation_id": m.mitigation_id,
                    "action_taken": m.action_taken,
                    "outcome": m.outcome,
                    "recommended_practice": m.recommended_preventive_practice,
                    "source_reference": m.source_reference
                }
                for m in e.mitigations
            ]
        }
        for e in well.events
    ]

    trajectory_sample = [
        {
            "md": t.md,
            "tvd": t.tvd,
            "tvdss": t.tvdss,
            "inclination": t.inclination,
            "azimuth": t.azimuth,
            "dogleg_severity": t.dogleg_severity
        }
        for t in well.trajectories[:30] # First 30 sample points
    ]

    return {
        "well_id": well.well_id,
        "name": well.name,
        "operator": well.operator,
        "field": well.field,
        "state": well.state,
        "district": well.district,
        "latitude": well.latitude,
        "longitude": well.longitude,
        "total_depth": well.total_depth,
        "spud_date": well.spud_date.isoformat() if well.spud_date else None,
        "completion_date": well.completion_date.isoformat() if well.completion_date else None,
        "well_type": well.well_type,
        "status": well.status,
        "formations": formations,
        "events": events,
        "trajectory_sample": trajectory_sample
    }
