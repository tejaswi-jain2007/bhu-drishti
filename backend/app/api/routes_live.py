from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.db.database import get_db
from app.db.models import DrillingTelemetry
from app.ml.anomaly_detector import anomaly_detector

router = APIRouter(prefix="/live", tags=["Real-Time Monitoring & Early Warning"])

class TelemetrySnapshot(BaseModel):
    well_id: str = "LIVE-BGJ-01"
    depth_md: float
    wob: float
    rpm: float
    torque: float
    rop: float
    spp: float
    flow_in: float
    mud_weight: float = 1.20
    hookload: Optional[float] = 1350.0

@router.get("/replay/{well_id}")
def get_replay_stream(
    well_id: str,
    limit: int = Query(200, description="Max telemetry records to retrieve for replay"),
    db: Session = Depends(get_db)
):
    """
    Retrieve historical high-frequency telemetry sequence to simulate live eRTMAC/WITSML streaming.
    """
    records = (
        db.query(DrillingTelemetry)
        .filter(DrillingTelemetry.well_id == well_id)
        .order_by(DrillingTelemetry.depth_md.asc())
        .limit(limit)
        .all()
    )
    if not records:
        # Fallback to any available telemetry well
        records = (
            db.query(DrillingTelemetry)
            .order_by(DrillingTelemetry.depth_md.asc())
            .limit(limit)
            .all()
        )

    results = []
    for r in records:
        results.append({
            "timestamp": r.timestamp.isoformat() if r.timestamp else None,
            "depth_md": r.depth_md,
            "wob": r.wob,
            "rpm": r.rpm,
            "torque": r.torque,
            "rop": r.rop,
            "spp": r.spp,
            "flow_in": r.flow_in,
            "mud_weight": r.mud_weight,
            "hookload": r.hookload,
            "is_anomaly": r.is_anomaly,
            "anomaly_type": r.anomaly_type
        })

    return {
        "well_id": well_id,
        "total_stream_points": len(results),
        "telemetry_stream": results
    }

@router.post("/evaluate")
def evaluate_realtime_point(point: TelemetrySnapshot):
    """
    Evaluate incoming real-time telemetry snapshot for early-warning hazard signatures.
    """
    alert = anomaly_detector.evaluate_telemetry_point(point.model_dump())
    return {
        "status": "evaluated",
        "has_alert": alert is not None,
        "alert": alert
    }
