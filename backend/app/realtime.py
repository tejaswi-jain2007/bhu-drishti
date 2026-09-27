from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from app.db.models.base import get_db
from app.services.monitoring_service import MonitoringService

router = APIRouter()

class SimulationStartRequest(BaseModel):
    well_id: int = 1
    start_depth: float = 2950.0
    inject_kick: bool = True
    kick_depth: float = 2992.0

@router.post("/simulate")
async def start_simulation(
    req: SimulationStartRequest,
    db: Session = Depends(get_db)
):
    """Start or initialize a real-time WITSML streaming simulation session"""
    service = MonitoringService(db)
    result = service.start_monitoring(req.well_id, start_depth_m=req.start_depth)
    return result

@router.get("/session/{session_id}/next")
async def get_next_telemetry_frame(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Fetch the next drilling telemetry frame and any triggered early warning alerts"""
    service = MonitoringService(db)
    frame = service.get_current_parameters(session_id)
    alerts = service.check_for_alerts(session_id)
    
    # Format alerts for frontend compatibility
    formatted_alerts = [
        {
            "alert_id": a.get("alert_id", "ALT-1"),
            "hazard_type": a.get("alert_type", "kick_influx"),
            "severity": a.get("severity", "critical"),
            "message": a.get("message", "Kick warning"),
            "depth_md": a.get("depth", frame.get("depth", 2992.0)),
            "timestamp": a.get("timestamp", ""),
            "recommended_immediate_action": a.get("recommended_action", "Space out and shut in well")
        }
        for a in alerts
    ]
    
    return {
        "status": "STREAMING",
        "depth": frame["depth"],
        "parameters": frame["parameters"],
        "alerts": formatted_alerts
    }

@router.delete("/session/{session_id}")
async def stop_simulation_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Stop active WITSML streaming session"""
    service = MonitoringService(db)
    return service.stop_monitoring(session_id)
