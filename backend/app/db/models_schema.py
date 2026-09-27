from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Well(Base):
    __tablename__ = "wells"

    well_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    operator = Column(String(100), default="Oil India Limited")
    field = Column(String(100), index=True)
    state = Column(String(100), index=True)
    district = Column(String(100), index=True)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    total_depth = Column(Float, nullable=False)
    spud_date = Column(DateTime, nullable=True)
    completion_date = Column(DateTime, nullable=True)
    well_type = Column(String(50), default="Exploratory")
    status = Column(String(50), default="Completed")

    formations = relationship("Formation", back_populates="well", cascade="all, delete-orphan")
    trajectories = relationship("WellTrajectory", back_populates="well", cascade="all, delete-orphan")
    events = relationship("DrillingEvent", back_populates="well", cascade="all, delete-orphan")
    telemetries = relationship("DrillingTelemetry", back_populates="well", cascade="all, delete-orphan")

    @property
    def trajectory(self):
        return self.trajectories

    @property
    def documents(self):
        return []

class WellTrajectory(Base):
    __tablename__ = "well_trajectories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    well_id = Column(String(50), ForeignKey("wells.well_id"), index=True)
    md = Column(Float, nullable=False)
    tvd = Column(Float, nullable=False)
    tvdss = Column(Float, nullable=True)
    inclination = Column(Float, default=0.0)
    azimuth = Column(Float, default=0.0)
    dogleg_severity = Column(Float, default=0.0)

    well = relationship("Well", back_populates="trajectories")

class Formation(Base):
    __tablename__ = "formations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    well_id = Column(String(50), ForeignKey("wells.well_id"), index=True)
    formation_name = Column(String(100), nullable=False, index=True)
    top_depth_md = Column(Float, nullable=False)
    base_depth_md = Column(Float, nullable=False)
    lithology = Column(String(100), nullable=False)
    porosity_avg = Column(Float, nullable=True)
    permeability_avg = Column(Float, nullable=True)
    description = Column(Text, nullable=True)

    well = relationship("Well", back_populates="formations")

    @property
    def top_depth(self):
        return self.top_depth_md

    @property
    def base_depth(self):
        return self.base_depth_md

    @property
    def age(self):
        return "Tertiary/Cenozoic"

class DrillingEvent(Base):
    __tablename__ = "drilling_events"

    event_id = Column(String(50), primary_key=True, index=True)
    well_id = Column(String(50), ForeignKey("wells.well_id"), index=True)
    event_type = Column(String(50), nullable=False, index=True)
    start_depth_md = Column(Float, nullable=False, index=True)
    end_depth_md = Column(Float, nullable=False)
    formation_name = Column(String(100), nullable=True)
    severity = Column(String(20), default="Moderate")
    npt_hours = Column(Float, default=0.0)
    description = Column(Text, nullable=False)
    root_cause = Column(Text, nullable=True)
    source_document = Column(String(200), nullable=True)
    page_number = Column(Integer, nullable=True)
    evidence_text = Column(Text, nullable=True)
    extraction_confidence = Column(Float, default=0.95)

    well = relationship("Well", back_populates="events")
    mitigations = relationship("Mitigation", back_populates="event", cascade="all, delete-orphan")

    @property
    def start_depth(self):
        return self.start_depth_md

    @property
    def end_depth(self):
        return self.end_depth_md

    @property
    def source(self):
        return self.source_document or "WCR/DDR"

    @property
    def confidence(self):
        return self.extraction_confidence

    @property
    def evidence(self):
        return []

class Mitigation(Base):
    __tablename__ = "mitigations"

    mitigation_id = Column(String(50), primary_key=True, index=True)
    event_id = Column(String(50), ForeignKey("drilling_events.event_id"), index=True)
    well_id = Column(String(50), index=True)
    action_taken = Column(Text, nullable=False)
    outcome = Column(Text, nullable=False)
    success_flag = Column(Boolean, default=True)
    recommended_preventive_practice = Column(Text, nullable=False)
    source_reference = Column(String(200), nullable=True)

    event = relationship("DrillingEvent", back_populates="mitigations")

    @property
    def action(self):
        return self.action_taken

    @property
    def source_document(self):
        return self.source_reference

class DrillingTelemetry(Base):
    __tablename__ = "drilling_telemetries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    well_id = Column(String(50), ForeignKey("wells.well_id"), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    depth_md = Column(Float, nullable=False, index=True)
    wob = Column(Float, nullable=False)
    rpm = Column(Float, nullable=False)
    torque = Column(Float, nullable=False)
    rop = Column(Float, nullable=False)
    spp = Column(Float, nullable=False)
    flow_in = Column(Float, nullable=False)
    mud_weight = Column(Float, nullable=False)
    hookload = Column(Float, nullable=True)
    is_anomaly = Column(Boolean, default=False)
    anomaly_type = Column(String(50), nullable=True)

    well = relationship("Well", back_populates="telemetries")

    @property
    def depth(self):
        return self.depth_md

    @property
    def flow(self):
        return self.flow_in

    @property
    def ecd(self):
        return self.mud_weight + 0.02

class WellSimilarity(Base):
    __tablename__ = "well_similarity"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source_well_id = Column(String(50), index=True)
    target_well_id = Column(String(50), index=True)
    similarity_score = Column(Float)

class RiskPrediction(Base):
    __tablename__ = "risk_predictions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    depth_start = Column(Float)
    depth_end = Column(Float)
    event_type = Column(String(50))
    probability = Column(Float)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    well_id = Column(String(50), index=True)
    severity = Column(String(20))
    title = Column(String(200))
    message = Column(Text)

# Aliases
WellLog = DrillingTelemetry
DrillingParameter = DrillingTelemetry
Event = DrillingEvent

class EventEvidence:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

class Document:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
