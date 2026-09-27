from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import wells, events, risk, assistant, ingestion, alerts, recommendations, realtime

app = FastAPI(
    title="Nearby Wells Intelligence System (NWIS)",
    description="AI/ML-enabled decision-support platform for drilling intelligence",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include standalone routers (handles /wells/districts, flex queries for /wells/nearby, etc.)
app.include_router(wells.router, prefix="/api/v1/wells", tags=["wells"])
app.include_router(events.router, prefix="/api/v1/events", tags=["events"])
app.include_router(risk.router, prefix="/api/v1/risk", tags=["risk"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["recommendations"])
app.include_router(assistant.router, prefix="/api/v1/assistant", tags=["assistant"])
app.include_router(ingestion.router, prefix="/api/v1/ingestion", tags=["ingestion"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["alerts"])
app.include_router(realtime.router, prefix="/api/v1/realtime", tags=["realtime"])

from app.api.api_router import api_router

# Include API v1 router suite
app.include_router(api_router, prefix="/api/v1")

from app.db.database import get_db

@app.get("/")
async def root():
    return {
        "message": "NWIS API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/api/v1/provinces")
async def get_provinces_root(db = Depends(get_db)):
    from app.services.spatial_service import SpatialService
    return SpatialService.get_distinct_locations(db)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
