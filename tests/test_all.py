import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.db.database import SessionLocal
from backend.app.services.spatial_service import SpatialService
from backend.app.services.risk_service import RiskService
from backend.app.services.rag_service import DrillingRAGAssistant
from backend.app.ml.anomaly_detector import anomaly_detector

client = TestClient(app)

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Operational"
    assert "Nearby Wells Intelligence System" in data["system"]

def test_spatial_service():
    db = SessionLocal()
    # Query Baghjan area
    wells = SpatialService.get_nearby_wells(db, latitude=27.5921, longitude=95.3942, radius_km=30.0)
    db.close()
    assert len(wells) > 0
    assert any("Baghjan" in w["name"] for w in wells)
    assert wells[0]["distance_km"] <= wells[-1]["distance_km"]

def test_risk_service():
    db = SessionLocal()
    risk_profile = RiskService.generate_depth_risk_profile(
        db=db,
        target_lat=27.5921,
        target_lon=95.3942,
        planned_depth=4000.0,
        interval_step_m=500.0,
        search_radius_km=30.0
    )
    db.close()
    assert "depth_intervals" in risk_profile
    assert len(risk_profile["depth_intervals"]) > 0
    assert "overall_summary" in risk_profile
    assert risk_profile["overall_summary"]["overall_risk_level"] in ["LOW", "MODERATE", "HIGH", "CRITICAL"]

def test_rag_assistant():
    db = SessionLocal()
    res = DrillingRAGAssistant.answer_query(db, "Show nearby wells with mud loss in Tipam")
    db.close()
    assert "answer" in res
    assert "citations" in res
    assert len(res["citations"]) > 0
    assert res["confidence"] > 0.5

def test_anomaly_detector_kick():
    # Simulate kick signature: high ROP and low SPP
    telemetry = {
        "depth_md": 2992.0,
        "rop": 35.0,
        "spp": 160.0,
        "torque": 15.0,
        "flow_in": 680.0,
        "mud_weight": 1.20
    }
    alert = anomaly_detector.evaluate_telemetry_point(telemetry)
    assert alert is not None
    assert alert["severity"] == "CRITICAL"
    assert "Kick" in alert["hazard_type"]

def test_anomaly_detector_normal():
    # Normal drilling
    telemetry = {
        "depth_md": 2500.0,
        "rop": 14.0,
        "spp": 185.0,
        "torque": 13.0,
        "flow_in": 650.0,
        "mud_weight": 1.20
    }
    alert = anomaly_detector.evaluate_telemetry_point(telemetry)
    assert alert is None
