from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import Well
from geopy.distance import geodesic
from typing import List, Dict, Optional
import math

def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in kilometers using haversine formula."""
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers

def calculate_bearing(point1: tuple, point2: tuple) -> float:
    """Calculate the initial compass bearing from point1 (lat, lon) to point2 (lat, lon) in degrees."""
    lat1, lon1 = math.radians(point1[0]), math.radians(point1[1])
    lat2, lon2 = math.radians(point2[0]), math.radians(point2[1])
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(dlon))
    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    return (initial_bearing + 360) % 360


class SpatialService:
    def __init__(self, db: Session):
        self.db = db
    
    @staticmethod
    def get_distinct_locations(db: Session) -> Dict[str, List[str]]:
        """Retrieve distinct states and districts present in the well database."""
        records = db.query(Well.state, Well.district).filter(Well.state.isnot(None)).distinct().all()
        locations = {}
        for state, district in records:
            if not state:
                continue
            if state not in locations:
                locations[state] = []
            if district and district not in locations[state]:
                locations[state].append(district)
        return locations

    @staticmethod
    def get_nearby_wells(
        db: Session,
        latitude: float,
        longitude: float,
        radius_km: float = 25.0,
        state: Optional[str] = None,
        district: Optional[str] = None
    ) -> List[Dict]:
        service = SpatialService(db)
        return service.find_nearby_wells(latitude, longitude, radius_km * 1000.0, state=state, district=district)

    def find_nearby_wells(
        self,
        latitude: float,
        longitude: float,
        radius: float,
        state: Optional[str] = None,
        district: Optional[str] = None
    ) -> List[Dict]:
        """Find wells within specified radius (in meters)"""
        lat_delta = radius / 111000.0
        lon_delta = radius / (111000.0 * math.cos(math.radians(latitude)))
        
        min_lat = latitude - lat_delta
        max_lat = latitude + lat_delta
        min_lon = longitude - lon_delta
        max_lon = longitude + lon_delta
        
        query = self.db.query(Well).filter(
            Well.latitude >= min_lat,
            Well.latitude <= max_lat,
            Well.longitude >= min_lon,
            Well.longitude <= max_lon
        )
        if state:
            query = query.filter(Well.state.ilike(f"%{state}%"))
        if district:
            query = query.filter(Well.district.ilike(f"%{district}%"))
            
        wells = query.all()
        
        nearby_wells = []
        proposed_point = (latitude, longitude)
        
        for well in wells:
            well_point = (well.latitude, well.longitude)
            distance = geodesic(proposed_point, well_point).meters
            
            if distance <= radius:
                bearing = calculate_bearing(proposed_point, well_point)
                direction = self._bearing_to_direction(bearing)
                event_count = len(well.events) if hasattr(well, 'events') and well.events else 0
                
                nearby_wells.append({
                    "well_id": well.well_id,
                    "name": well.name,
                    "operator": getattr(well, "operator", "Oil India Limited"),
                    "latitude": well.latitude,
                    "longitude": well.longitude,
                    "state": getattr(well, "state", "Assam"),
                    "district": getattr(well, "district", "Dibrugarh"),
                    "well_type": getattr(well, "well_type", "Exploratory"),
                    "distance": round(distance, 2),
                    "bearing": round(bearing, 2),
                    "direction": direction,
                    "total_depth": getattr(well, "total_depth", 3500.0),
                    "spud_year": well.spud_date.year if getattr(well, 'spud_date', None) else None,
                    "field": getattr(well, "field", "Upper Assam"),
                    "block": getattr(well, "block", None),
                    "historical_events_count": event_count
                })
        
        nearby_wells.sort(key=lambda x: x["distance"])
        return nearby_wells
    
    def _bearing_to_direction(self, bearing: float) -> str:
        """Convert bearing angle to cardinal direction"""
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        index = round(bearing / 45) % 8
        return directions[index]
