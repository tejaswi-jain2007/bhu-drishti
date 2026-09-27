from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.db.models.base import get_db
from app.ingestion.csv.well_ingester import WellCSVIngester
from app.ingestion.csv.event_ingester import EventCSVIngester
import os

router = APIRouter()

@router.post("/csv/wells")
async def ingest_wells_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Ingest wells from a CSV file"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    # Save uploaded file temporarily
    temp_path = f"data/raw/temp_{file.filename}"
    os.makedirs("data/raw", exist_ok=True)
    
    try:
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        ingester = WellCSVIngester(db)
        wells_added = ingester.ingest_wells_from_csv(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return {
            "message": f"Successfully ingested {wells_added} wells",
            "wells_added": wells_added
        }
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/csv/formations")
async def ingest_formations_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Ingest formations from a CSV file"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    temp_path = f"data/raw/temp_{file.filename}"
    os.makedirs("data/raw", exist_ok=True)
    
    try:
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        ingester = WellCSVIngester(db)
        formations_added = ingester.ingest_formations_from_csv(temp_path)
        
        os.remove(temp_path)
        
        return {
            "message": f"Successfully ingested {formations_added} formations",
            "formations_added": formations_added
        }
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/csv/events")
async def ingest_events_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Ingest events from a CSV file"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    temp_path = f"data/raw/temp_{file.filename}"
    os.makedirs("data/raw", exist_ok=True)
    
    try:
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        ingester = EventCSVIngester(db)
        events_added = ingester.ingest_events_from_csv(temp_path)
        
        os.remove(temp_path)
        
        return {
            "message": f"Successfully ingested {events_added} events",
            "events_added": events_added
        }
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/load-sample-data")
async def load_sample_data(db: Session = Depends(get_db)):
    """Load comprehensive Pan-India benchmark data covering Assam, MP, Gujarat, Rajasthan, etc."""
    try:
        from app.db.seed_pan_india import seed_pan_india_database
        from app.db.models.well import Well
        from app.db.models.event import Event

        seed_pan_india_database(db, force=True)
        wells_count = db.query(Well).count()
        events_count = db.query(Event).count()

        return {
            "message": "Pan-India benchmark dataset successfully seeded",
            "wells_count": wells_count,
            "events_count": events_count,
            "status": "Ready"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
