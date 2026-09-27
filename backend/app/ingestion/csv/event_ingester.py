import pandas as pd
from sqlalchemy.orm import Session
from app.db.models.well import Well
from app.db.models.event import Event, Mitigation
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventCSVIngester:
    """Ingest event data from CSV files"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def ingest_events_from_csv(self, file_path: str) -> int:
        """Ingest events from a CSV file"""
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} events from CSV")
            
            events_added = 0
            for _, row in df.iterrows():
                # Find the well by name
                well = self.db.query(Well).filter(Well.name == row.get('well_name')).first()
                
                if well:
                    event = Event(
                        well_id=well.well_id,
                        event_type=row.get('event_type', ''),
                        start_depth=float(row.get('start_depth', 0)),
                        end_depth=float(row.get('end_depth')) if pd.notna(row.get('end_depth')) else None,
                        severity=row.get('severity'),
                        description=row.get('description'),
                        npt_hours=float(row.get('npt_hours')) if pd.notna(row.get('npt_hours')) else None,
                        mitigation_successful=bool(row.get('mitigation_successful', False)),
                        source=row.get('source', 'csv'),
                        confidence=float(row.get('confidence', 1.0))
                    )
                    
                    self.db.add(event)
                    events_added += 1
                else:
                    logger.warning(f"Well {row.get('well_name')} not found, skipping event")
            
            self.db.commit()
            logger.info(f"Successfully added {events_added} events")
            return events_added
            
        except Exception as e:
            logger.error(f"Error ingesting events: {e}")
            self.db.rollback()
            raise