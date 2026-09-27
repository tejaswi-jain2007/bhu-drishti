from sqlalchemy.orm import Session
from app.db.models.well import Well, Formation
from app.db.models.event import Event
from app.services.spatial_service import SpatialService
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CorrelationService:
    """Service for cross-well correlation and stratigraphic incident alignment (FR-09)"""

    def __init__(self, db: Session):
        self.db = db

    def get_cross_well_correlation(
        self,
        latitude: float,
        longitude: float,
        planned_depth: float,
        radius: float = 50000.0,
        limit_wells: int = 5
    ) -> Dict:
        """
        Correlate nearby wells with the proposed location by:
        1. Discovering nearby offset wells
        2. Extracting and aligning stratigraphic formation tops
        3. Mapping historical drilling incidents to formation intervals
        4. Highlighting regional hazard hot-zones
        """
        spatial_service = SpatialService(self.db)
        nearby = spatial_service.find_nearby_wells(latitude, longitude, radius)

        if not nearby:
            return {
                "proposed_well": {
                    "latitude": latitude,
                    "longitude": longitude,
                    "planned_depth": planned_depth
                },
                "correlated_wells": [],
                "stratigraphic_hotspots": []
            }

        selected_nearby = nearby[:limit_wells]
        correlated_wells = []
        all_formation_names = set()
        formation_incident_map = {}

        for n_well in selected_nearby:
            well_id = n_well["well_id"]
            well = self.db.query(Well).filter(Well.well_id == well_id).first()
            if not well:
                continue

            # Formations
            formations_db = self.db.query(Formation).filter(Formation.well_id == well_id).order_by(Formation.top_depth).all()
            formations = [
                {
                    "formation_name": f.formation_name,
                    "top_depth": f.top_depth,
                    "base_depth": f.base_depth,
                    "lithology": f.lithology,
                    "description": f.description
                }
                for f in formations_db
            ]

            # Events
            events_db = self.db.query(Event).filter(Event.well_id == well_id).order_by(Event.start_depth).all()
            events = []
            for ev in events_db:
                # Find matching formation
                matched_formation = "Unknown"
                for f in formations:
                    if f["top_depth"] <= ev.start_depth <= (f["base_depth"] or f["top_depth"] + 500):
                        matched_formation = f["formation_name"]
                        break

                ev_dict = {
                    "event_id": ev.event_id,
                    "event_type": ev.event_type,
                    "start_depth": ev.start_depth,
                    "end_depth": ev.end_depth,
                    "severity": ev.severity,
                    "description": ev.description,
                    "formation": matched_formation,
                    "npt_hours": ev.npt_hours,
                    "mitigation_successful": ev.mitigation_successful
                }
                events.append(ev_dict)

                # Aggregate hotspot
                if matched_formation not in formation_incident_map:
                    formation_incident_map[matched_formation] = {
                        "formation": matched_formation,
                        "incident_count": 0,
                        "event_types": set(),
                        "wells": set(),
                        "min_depth": ev.start_depth,
                        "max_depth": ev.end_depth or ev.start_depth
                    }
                fm = formation_incident_map[matched_formation]
                fm["incident_count"] += 1
                fm["event_types"].add(ev.event_type)
                fm["wells"].add(well.name)
                fm["min_depth"] = min(fm["min_depth"], ev.start_depth)
                fm["max_depth"] = max(fm["max_depth"], ev.end_depth or ev.start_depth)

            correlated_wells.append({
                "well_id": well.well_id,
                "name": well.name,
                "operator": well.operator,
                "distance_km": round(n_well["distance"] / 1000.0, 2),
                "bearing_deg": n_well["bearing"],
                "direction": n_well["direction"],
                "total_depth": well.total_depth,
                "formations": formations,
                "events": events
            })

        # Format hotspots
        stratigraphic_hotspots = []
        for form_name, hot_data in formation_incident_map.items():
            stratigraphic_hotspots.append({
                "formation": form_name,
                "incident_count": hot_data["incident_count"],
                "event_types": list(hot_data["event_types"]),
                "wells_affected": list(hot_data["wells"]),
                "depth_range": f"{round(hot_data['min_depth'])}m - {round(hot_data['max_depth'])}m",
                "risk_level": "CRITICAL" if any(t in ["kick", "stuck_pipe"] for t in hot_data["event_types"]) else "HIGH"
            })

        stratigraphic_hotspots.sort(key=lambda x: x["incident_count"], reverse=True)

        return {
            "proposed_well": {
                "latitude": latitude,
                "longitude": longitude,
                "planned_depth": planned_depth,
                "search_radius_km": round(radius / 1000.0, 1)
            },
            "correlated_wells": correlated_wells,
            "stratigraphic_hotspots": stratigraphic_hotspots
        }
