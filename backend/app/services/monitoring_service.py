from sqlalchemy.orm import Session
from app.db.models.well import Well, DrillingParameter
from app.db.models.event import Event
from app.db.models.risk import Alert
from app.ml.anomaly_detector import anomaly_detector
from typing import List, Dict, Optional
import logging
from datetime import datetime, timedelta
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonitoringService:
    """Service for real-time drilling telemetry streaming and early-warning alerts (FR-17, FR-18, TRD Section 19)"""

    def __init__(self, db: Session):
        self.db = db
        # In-memory monitoring sessions
        if not hasattr(MonitoringService, "_active_monitors"):
            MonitoringService._active_monitors = {}
        self.active_monitors = MonitoringService._active_monitors

    def start_monitoring(self, well_id: int, start_depth_m: float = 2950.0) -> Dict:
        """Start a WITSML telemetry streaming simulation session for a well"""
        well = self.db.query(Well).filter(Well.well_id == well_id).first()
        well_name = well.name if well else f"Well-{well_id}"

        session_id = f"monitor_{well_id}_{int(datetime.utcnow().timestamp())}"
        self.active_monitors[session_id] = {
            "well_id": well_id,
            "well_name": well_name,
            "started_at": datetime.utcnow(),
            "current_depth": start_depth_m,
            "kick_target_depth": 2992.0,  # Signature kick at 2992m
            "step_count": 0,
            "parameters": self._initialize_parameters()
        }

        logger.info(f"Started monitoring session {session_id} for well {well_name} at depth {start_depth_m}m")
        return {
            "session_id": session_id,
            "well_id": well_id,
            "well_name": well_name,
            "status": "monitoring",
            "started_at": datetime.utcnow().isoformat(),
            "current_depth": start_depth_m
        }

    def stop_monitoring(self, session_id: str) -> Dict:
        """Stop an active monitoring session"""
        if session_id not in self.active_monitors:
            return {"session_id": session_id, "status": "stopped"}

        session = self.active_monitors.pop(session_id)
        return {
            "session_id": session_id,
            "status": "stopped",
            "stopped_at": datetime.utcnow().isoformat(),
            "final_depth": round(session["current_depth"], 2)
        }

    def get_current_parameters(self, session_id: str) -> Dict:
        """Advance drilling simulation step and return current WITSML parameter stream"""
        if session_id not in self.active_monitors:
            # Recreate session if expired
            self.start_monitoring(1)
            session_id = list(self.active_monitors.keys())[-1]

        session = self.active_monitors[session_id]
        session["step_count"] += 1

        # Advance depth by 1.5 to 3.0 meters
        session["current_depth"] += round(random.uniform(1.2, 2.8), 2)
        depth = session["current_depth"]

        # Check if depth enters the kick precursor zone (2988m - 2996m)
        is_kick_zone = 2988.0 <= depth <= 2996.0

        if is_kick_zone:
            rop = round(random.uniform(32.0, 39.5), 1)  # Sudden drilling break!
            spp = round(random.uniform(158.0, 168.0), 1)  # Pressure drop
            torque = round(random.uniform(16.5, 19.5), 1)
            wob = round(random.uniform(105.0, 118.0), 1)
            flow = round(random.uniform(690.0, 725.0), 1)
            pit_gain = round(random.uniform(18.0, 32.0), 1)  # Tank influx
            gas_pct = round(random.uniform(34.0, 48.0), 1)  # High gas peak
            mud_weight = 1.19
        else:
            rop = round(random.uniform(12.0, 16.5), 1)
            spp = round(random.uniform(182.0, 190.0), 1)
            torque = round(random.uniform(12.0, 14.5), 1)
            wob = round(random.uniform(130.0, 145.0), 1)
            flow = round(random.uniform(640.0, 660.0), 1)
            pit_gain = round(random.uniform(-1.0, 1.5), 1)
            gas_pct = round(random.uniform(1.2, 3.8), 1)
            mud_weight = 1.18

        session["parameters"] = {
            "rop": rop,
            "wob": wob,
            "rpm": 110.0,
            "torque": torque,
            "spp": spp,
            "flow": flow,
            "pit_gain": pit_gain,
            "gas_pct": gas_pct,
            "hookload": round(random.uniform(1120.0, 1160.0), 1),
            "mud_weight": mud_weight,
            "ecd": round(mud_weight + 0.05, 2)
        }

        return {
            "session_id": session_id,
            "well_id": session["well_id"],
            "well_name": session["well_name"],
            "timestamp": datetime.utcnow().isoformat(),
            "depth": round(depth, 1),
            "parameters": session["parameters"]
        }

    def check_for_alerts(self, session_id: str) -> List[Dict]:
        """Evaluate current telemetry snapshot against historical hazard patterns"""
        if session_id not in self.active_monitors:
            return []

        session = self.active_monitors[session_id]
        params = session["parameters"]
        depth = session["current_depth"]

        telemetry_payload = {
            "well_id": session["well_name"],
            "depth_md": depth,
            "rop": params["rop"],
            "spp": params["spp"],
            "torque": params["torque"],
            "flow": params["flow"],
            "mud_weight": params["mud_weight"],
            "pit_gain": params.get("pit_gain", 0.0),
            "gas_pct": params.get("gas_pct", 1.5),
            "wob": params["wob"]
        }

        alert = anomaly_detector.evaluate_telemetry_point(telemetry_payload)
        if alert:
            return [alert]
        return []

    def _initialize_parameters(self) -> Dict:
        return {
            "rop": 14.0,
            "wob": 135.0,
            "rpm": 110.0,
            "torque": 13.5,
            "spp": 185.0,
            "flow": 650.0,
            "pit_gain": 0.0,
            "gas_pct": 2.1,
            "hookload": 1140.0,
            "mud_weight": 1.18,
            "ecd": 1.23
        }