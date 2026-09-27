from fastapi import APIRouter
from app.api.routes_wells import router as wells_router
from app.api.routes_risk import router as risk_router
from app.api.routes_assistant import router as assistant_router
from app.api.routes_live import router as live_router

api_router = APIRouter()

api_router.include_router(wells_router)
api_router.include_router(risk_router)
api_router.include_router(assistant_router)
api_router.include_router(live_router)
