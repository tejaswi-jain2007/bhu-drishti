from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.db.models.base import get_db
from app.services.monitoring_service import MonitoringService
import json

router = APIRouter()

class MonitoringSession(BaseModel):
    well_id: int

class MonitoringResponse(BaseModel):
    session_id: str
    well_id: int
    well_name: str
    status: str
    started_at: str

# Global monitoring service instance
monitoring_service = None

def get_monitoring_service():
    global monitoring_service
    if monitoring_service is None:
        from app.db.models.base import SessionLocal
        db = SessionLocal()
        monitoring_service = MonitoringService(db)
    return monitoring_service

@router.post("/monitoring/start")
async def start_monitoring(session: MonitoringSession):
    """Start real-time monitoring for a well"""
    try:
        service = get_monitoring_service()
        result = service.start_monitoring(session.well_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/monitoring/stop/{session_id}")
async def stop_monitoring(session_id: str):
    """Stop a monitoring session"""
    try:
        service = get_monitoring_service()
        result = service.stop_monitoring(session_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monitoring/parameters/{session_id}")
async def get_current_parameters(session_id: str):
    """Get current drilling parameters for a monitoring session"""
    try:
        service = get_monitoring_service()
        result = service.get_current_parameters(session_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monitoring/alerts/{session_id}")
async def check_alerts(session_id: str):
    """Check for alerts in current monitoring session"""
    try:
        service = get_monitoring_service()
        alerts = service.check_for_alerts(session_id)
        return {
            "session_id": session_id,
            "alerts": alerts,
            "alert_count": len(alerts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monitoring/replay/{well_id}")
async def get_historical_replay(well_id: int, start_depth: float = 0, end_depth: float = 3000):
    """Get historical drilling data for replay simulation"""
    try:
        service = get_monitoring_service()
        data = service.get_historical_data_replay(well_id, start_depth, end_depth)
        return {
            "well_id": well_id,
            "start_depth": start_depth,
            "end_depth": end_depth,
            "data_points": len(data),
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws/monitoring/{session_id}")
async def websocket_monitoring(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time monitoring updates"""
    await websocket.accept()
    
    try:
        service = get_monitoring_service()
        
        while True:
            # Get current parameters
            parameters = service.get_current_parameters(session_id)
            
            # Check for alerts
            alerts = service.check_for_alerts(session_id)
            
            # Send update
            await websocket.send_json({
                "type": "monitoring_update",
                "session_id": session_id,
                "parameters": parameters,
                "alerts": alerts
            })
            
            # Wait before next update (simulating real-time)
            import asyncio
            await asyncio.sleep(2)  # 2 second intervals
            
    except WebSocketDisconnect:
        print(f"Client disconnected from session {session_id}")
    except Exception as e:
        print(f"Error in monitoring websocket: {e}")
        await websocket.close()
