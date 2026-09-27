import pandas as pd
from sqlalchemy.orm import Session
from app.db.models.well import Well, Formation
from app.db.models.base import Base
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WellCSVIngester:
    """Ingest well data from CSV files"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def ingest_wells_from_csv(self, file_path: str) -> int:
        """Ingest wells from a CSV file"""
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} wells from CSV")
            
            wells_added = 0
            for _, row in df.iterrows():
                well = Well(
                    name=row.get('name', ''),
                    operator=row.get('operator', ''),
                    latitude=float(row.get('latitude', 0)),
                    longitude=float(row.get('longitude', 0)),
                    total_depth=float(row.get('total_depth', 0)) if pd.notna(row.get('total_depth')) else None,
                    well_type=row.get('well_type'),
                    field=row.get('field'),
                    block=row.get('block'),
                    country=row.get('country', 'India'),
                    state=row.get('state', 'Assam'),
                    district=row.get('district')
                )
                
                self.db.add(well)
                wells_added += 1
            
            self.db.commit()
            logger.info(f"Successfully added {wells_added} wells")
            return wells_added
            
        except Exception as e:
            logger.error(f"Error ingesting wells: {e}")
            self.db.rollback()
            raise
    
    def ingest_formations_from_csv(self, file_path: str) -> int:
        """Ingest formation data from a CSV file"""
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} formations from CSV")
            
            formations_added = 0
            for _, row in df.iterrows():
                # Find the well by name
                well = self.db.query(Well).filter(Well.name == row.get('well_name')).first()
                
                if well:
                    formation = Formation(
                        well_id=well.well_id,
                        formation_name=row.get('formation_name', ''),
                        top_depth=float(row.get('top_depth', 0)),
                        base_depth=float(row.get('base_depth')) if pd.notna(row.get('base_depth')) else None,
                        lithology=row.get('lithology'),
                        age=row.get('age'),
                        description=row.get('description')
                    )
                    
                    self.db.add(formation)
                    formations_added += 1
                else:
                    logger.warning(f"Well {row.get('well_name')} not found, skipping formation")
            
            self.db.commit()
            logger.info(f"Successfully added {formations_added} formations")
            return formations_added
            
        except Exception as e:
            logger.error(f"Error ingesting formations: {e}")
            self.db.rollback()
            raise