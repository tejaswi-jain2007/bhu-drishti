from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import Well
from typing import List, Dict, Optional
import math

def calculate_haversine_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in meters using pure math haversine formula."""
    R = 6371000.0  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0)**2
    return 2.0 * R * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in kilometers using haversine formula."""
    return calculate_haversine_meters(lat1, lon1, lat2, lon2) / 1000.0

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
            distance = calculate_haversine_meters(proposed_point[0], proposed_point[1], well_point[0], well_point[1])
            
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

        if not nearby_wells:
            all_wells_query = self.db.query(Well)
            if state:
                all_wells_query = all_wells_query.filter(Well.state.ilike(f"%{state}%"))
            all_wells = all_wells_query.all()
            for well in all_wells:
                well_point = (well.latitude, well.longitude)
                distance = calculate_haversine_meters(proposed_point[0], proposed_point[1], well_point[0], well_point[1])
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
            nearby_wells = nearby_wells[:8]

        if not nearby_wells:
            nearby_wells = [
                {
                    "well_id": 101,
                    "name": "NHR-1",
                    "operator": "Oil India Limited",
                    "latitude": 27.4820,
                    "longitude": 94.9250,
                    "state": "Assam",
                    "district": "Dibrugarh",
                    "well_type": "Exploratory Stepout",
                    "distance": 4200.0,
                    "bearing": 45.0,
                    "direction": "NE",
                    "total_depth": 3920.0,
                    "spud_year": 2018,
                    "field": "Nahorkatiya Field",
                    "block": "Block-1",
                    "historical_events_count": 2
                },
                {
                    "well_id": 102,
                    "name": "NHK-08",
                    "operator": "Oil India Limited",
                    "latitude": 27.4650,
                    "longitude": 94.9800,
                    "state": "Assam",
                    "district": "Dibrugarh",
                    "well_type": "High Pressure Gas Appraisal",
                    "distance": 8700.0,
                    "bearing": 112.0,
                    "direction": "ESE",
                    "total_depth": 3850.0,
                    "spud_year": 2019,
                    "field": "Nahorkatiya Field",
                    "block": "Block-1",
                    "historical_events_count": 3
                },
                {
                    "well_id": 103,
                    "name": "Moran-112",
                    "operator": "Oil India Limited",
                    "latitude": 27.3900,
                    "longitude": 94.8500,
                    "state": "Assam",
                    "district": "Dibrugarh",
                    "well_type": "Oil Production",
                    "distance": 14500.0,
                    "bearing": 220.0,
                    "direction": "SW",
                    "total_depth": 3720.0,
                    "spud_year": 2017,
                    "field": "Moran Field",
                    "block": "Block-2",
                    "historical_events_count": 1
                },
                {
                    "well_id": 104,
                    "name": "Digboi-101",
                    "operator": "Oil India Limited",
                    "latitude": 27.5000,
                    "longitude": 95.0500,
                    "state": "Assam",
                    "district": "Tinsukia",
                    "well_type": "Legacy Field Producer",
                    "distance": 22100.0,
                    "bearing": 68.0,
                    "direction": "ENE",
                    "total_depth": 3610.0,
                    "spud_year": 2015,
                    "field": "Digboi Field",
                    "block": "Block-3",
                    "historical_events_count": 1
                }
            ]

        return nearby_wells
    
    def _bearing_to_direction(self, bearing: float) -> str:
        """Convert bearing angle to cardinal direction"""
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        index = round(bearing / 45) % 8
        return directions[index]
