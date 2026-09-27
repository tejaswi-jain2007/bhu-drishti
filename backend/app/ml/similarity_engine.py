import math
from typing import List, Dict, Any, Optional
try:
    from sqlalchemy.orm import Session
except ImportError:
    Session = Any  # type: ignore
from app.db.models import Well, Formation
from app.services.spatial_service import calculate_haversine_distance

class WellSimilarityEngine:
    @staticmethod
    def compute_similarity(
        db: Session,
        target_lat: float,
        target_lon: float,
        planned_depth: float,
        target_formations: Optional[List[str]] = None,
        candidate_wells: Optional[List[Dict[str, Any]]] = None,
        max_dist_km: float = 50.0
    ) -> List[Dict[str, Any]]:
        """
        Rank candidate wells based on spatial proximity, target depth alignment, and geological formation overlap.
        """
        if candidate_wells is None:
            db_wells = db.query(Well).all()
        else:
            well_ids = [w["well_id"] for w in candidate_wells]
            db_wells = db.query(Well).filter(Well.well_id.in_(well_ids)).all()

        scored_wells = []

        for w in db_wells:
            dist_km = calculate_haversine_distance(target_lat, target_lon, w.latitude, w.longitude)
            if dist_km > max_dist_km:
                continue

            # 1. Spatial similarity score (decay function)
            # Distance of 0km -> 1.0, 15km -> 0.37, 30km -> 0.13
            spatial_score = math.exp(-dist_km / 15.0)

            # 2. Depth similarity score
            depth_diff = abs(planned_depth - w.total_depth)
            depth_score = max(0.0, 1.0 - (depth_diff / 1500.0))

            # 3. Geological formation overlap score
            well_formations = [f.formation_name for f in w.formations]
            if target_formations and len(target_formations) > 0 and len(well_formations) > 0:
                set_target = set([f.lower().strip() for f in target_formations])
                set_offset = set([f.lower().strip() for f in well_formations])
                intersection = set_target.intersection(set_offset)
                union = set_target.union(set_offset)
                geo_score = len(intersection) / len(union) if union else 0.5
            else:
                # Default high geological confidence if in the same field/basin
                geo_score = 0.8 if spatial_score > 0.4 else 0.5

            # Composite Multi-factor Score
            composite_score = (0.45 * spatial_score) + (0.30 * depth_score) + (0.25 * geo_score)
            composite_score = round(min(1.0, max(0.0, composite_score)), 3)

            scored_wells.append({
                "well_id": w.well_id,
                "name": w.name,
                "field": w.field,
                "operator": w.operator,
                "distance_km": round(dist_km, 2),
                "total_depth": w.total_depth,
                "composite_similarity": composite_score,
                "breakdown": {
                    "spatial_proximity_score": round(spatial_score, 3),
                    "depth_alignment_score": round(depth_score, 3),
                    "geological_overlap_score": round(geo_score, 3)
                },
                "formations": well_formations,
                "historical_events_count": len(w.events)
            })

        # Sort by highest composite similarity
        scored_wells.sort(key=lambda x: x["composite_similarity"], reverse=True)
        return scored_wells
