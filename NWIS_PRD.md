# Product Requirements Document (PRD)
## Nearby Wells Intelligence System (NWIS)
### Oil India Limited — SIH 2026

**Version:** 1.0  
**Status:** SIH Prototype / Product Definition

---

## 1. Product Overview

The Nearby Wells Intelligence System (NWIS) is an AI/ML-enabled decision-support platform designed to convert historical drilling knowledge into actionable intelligence for a proposed or active well.

The system helps drilling and geology teams answer questions such as:

- Which historical wells are nearby?
- What happened in those wells at similar depths or formations?
- Which drilling problems were observed?
- Are similar problems historically associated with the proposed location?
- Which depth intervals deserve additional attention?
- What preventive practices were used successfully in similar wells?
- During drilling, is the current behavior starting to resemble historical risk patterns?

NWIS is intended to operate alongside an operational drilling platform such as eRTMAC. It is a decision-support and early-warning system, not an autonomous drilling controller.

---

## 2. Problem Definition

Historical well knowledge is often distributed across WCRs, DDRs, mud logging records, PDFs, drilling databases, well trajectories, geological records and individual engineering experience.

This creates several problems:

1. Historical knowledge is difficult to retrieve quickly.
2. Similar nearby wells may not be identified early enough.
3. Drilling events may not be compared consistently by depth and formation.
4. Preventive lessons may remain buried inside documents.
5. Engineers may have to manually review multiple reports before making a decision.
6. During live drilling, historical context may not be available in the same workflow.

NWIS addresses this by building a searchable institutional-memory layer and connecting it with geospatial, geological, drilling and real-time information.

---

## 3. Objectives

### Primary Objectives

- Provide a geospatial view of nearby historical wells.
- Search and retrieve historical well experiences.
- Correlate events with depth and formation.
- Build a depth-wise risk profile for a proposed well.
- Provide evidence-backed preventive recommendations.
- Support natural-language questions through an AI assistant.
- Prepare the architecture for real-time eRTMAC/WITSML monitoring.

### Secondary Objectives

- Preserve source provenance for every insight.
- Reduce time required to find relevant historical information.
- Standardize drilling event taxonomy.
- Enable future model retraining using authorized Oil India data.

---

## 4. Target Users

### Drilling Engineer
Needs nearby-well intelligence, event history, risk intervals and preventive recommendations.

### Geologist
Needs geological similarity, formation information and historical well comparison.

### Drilling Supervisor / Operations Team
Needs quick risk visibility and real-time alerts.

### Data / AI Analyst
Needs structured historical events, model outputs and data-quality information.

### Administrator
Needs user management, access control, data ingestion and audit functions.

---

## 5. End-to-End User Journey

1. User opens NWIS.
2. User selects the State.
3. User selects the District.
4. System displays the district map.
5. User selects the exact proposed drilling location.
6. User enters planned drilling depth.
7. User enters or selects known soil/geological information.
8. User defines the search radius.
9. System searches historical wells within that radius.
10. System displays nearby wells with distance, direction and drilling year.
11. User opens individual well profiles.
12. System shows historical events by depth and formation.
13. System correlates similar historical events with the proposed location.
14. System generates a depth-wise risk profile.
15. System considers available environmental/weather context where relevant.
16. System presents historical hydrocarbon evidence where available.
17. System highlights depth intervals with repeated historical problems.
18. System provides preventive recommendations based on historical evidence.
19. System may present alternative candidate locations when configured and supported by available evidence.
20. Once drilling begins, live eRTMAC/WITSML data can be compared against historical patterns.
21. The system generates early warnings when configured thresholds/models indicate similarity to historical risk patterns.
22. User can ask the AI assistant natural-language questions.

---

## 6. Functional Requirements

### FR-01 — State & District Selection
The system shall allow the user to select a State and District before creating a proposed drilling location.

### FR-02 — Map-Based Location Selection
The system shall display a map and allow the user to pinpoint the proposed drilling coordinates.

### FR-03 — Planned Depth Input
The system shall capture approximate planned drilling depth.

### FR-04 — Geological Input
The system shall capture available soil, geological, formation or lithology information.

### FR-05 — Nearby Well Discovery
The system shall search for historical wells within a configurable radius.

### FR-06 — Historical Well Profile
Each well profile shall include available metadata, trajectory, depth, formations and historical events.

### FR-07 — Document Intelligence
The system shall ingest and process relevant historical documents such as WCRs, DDRs and drilling reports when authorized data is available.

### FR-08 — Event Extraction
The system shall structure relevant drilling events such as:

- Mud losses
- Kicks
- Stuck pipe
- Fishing
- Pressure anomalies
- Torque/drag anomalies
- Casing issues
- Cementing issues
- Non-productive time events

### FR-09 — Cross-Well Correlation
The system shall correlate events across wells by location, depth, formation and available drilling parameters.

### FR-10 — Depth-Wise Risk Profile
The system shall visualize historical/model-supported risk over planned depth intervals.

### FR-11 — Risk Probability
Where adequate validated training data exists, the system may provide model-based event probability estimates.

### FR-12 — Environmental Context
The system may use recent environmental/weather conditions as contextual features where physically relevant and supported by data.

### FR-13 — Location Assessment
The system shall summarize the historical and model-supported risk profile of the selected location.

### FR-14 — Alternative Locations
Where configured and sufficiently supported by data, the system may compare candidate locations and present lower-risk historical/modelled alternatives.

### FR-15 — Hydrocarbon Evidence
The system shall display historical evidence of hydrocarbon occurrence in nearby wells where data is available. It shall not guarantee hydrocarbon discovery.

### FR-16 — Preventive Recommendations
The system shall surface historical mitigation practices associated with similar events.

### FR-17 — Real-Time Monitoring
The architecture shall support ingestion of live drilling parameters from authorized eRTMAC/WITSML or equivalent sources.

### FR-18 — Early Warning
The system shall generate alerts when configured rules or validated ML models detect patterns associated with historical risks.

### FR-19 — AI Assistant
The system shall support natural-language search and evidence-backed answers.

Example:
> “Show nearby wells that experienced mud loss around 2800 m.”

---

## 7. Key Product Modules

### 7.1 Location & Planning Module
- State/district selection
- Map
- Proposed well coordinates
- Planned depth
- Geological inputs
- Search radius

### 7.2 Nearby Wells Module
- Nearby well discovery
- Distance
- Direction
- Well age/year
- Historical summary

### 7.3 Historical Intelligence Module
- WCR/DDRs
- Drilling reports
- Well logs
- Event timeline
- Formation context
- Mitigation history

### 7.4 Risk Intelligence Module
- Depth-wise risk
- Historical event frequency
- Comparable-well evidence
- Model probabilities where validated
- Confidence and data quality

### 7.5 Recommendation Module
- Preventive practices
- Historical mitigation actions
- Source references
- Confidence

### 7.6 Real-Time Monitoring Module
- Live drilling parameters
- Historical pattern comparison
- Anomaly detection
- Early warnings

### 7.7 AI Assistant
- Natural-language queries
- Hybrid search
- Source citations
- Evidence-based summaries

---

## 8. Historical Data Requirements

The system should be able to work with, where authorized:

- WCRs
- DDRs
- Mud logging reports
- Drilling reports
- Well headers
- Well trajectories
- Formation tops
- Geological data
- Casing/cementing programs
- Mud programs
- BHA/bit information
- Historical drilling incidents
- Reservoir/geological data
- eRTMAC/WITSML streams

---

## 9. Data Strategy for SIH Prototype

Oil India proprietary operational data should not be assumed to be publicly available.

### Open Data Sources

The SIH prototype can use legally accessible public datasets such as:

- Equinor Volve Open Data
- NLOG Netherlands public borehole and geological datasets
- NLOG PSNS pressure-related data

### Authorized Production Data

Production deployment can add:

- Oil India WCR/DDR data
- Authorized historical event data
- Approved eRTMAC feeds
- Internal well/log databases

### Synthetic / Derived Data

Where a required event label is unavailable, the prototype may use:

- Rule-derived labels
- Expert-reviewed annotations
- Clearly marked synthetic data

Synthetic data must never be presented as actual Oil India observations.

---

## 10. AI / ML Requirements

The product should use modular AI/ML components rather than one monolithic model.

### Required Components

- Comparable-well retrieval
- Event classification
- Depth-risk estimation
- Anomaly detection
- Document/event extraction
- Vector retrieval
- Evidence ranking
- AI assistant

### Example Feature Groups

**Spatial**
- Distance
- Bearing
- Field/block membership

**Geological**
- Formation
- Lithology
- Porosity/permeability
- Available log curves

**Drilling**
- Depth
- ROP
- WOB
- RPM
- Torque
- SPP
- Flow
- Hookload
- Mud weight
- ECD where available

**Historical**
- Event type
- Event depth
- Severity
- NPT
- Mitigation outcome

**Trajectory**
- Inclination
- Azimuth
- Dogleg severity

---

## 11. Risk Output

The UI should provide a depth-wise profile such as:

| Depth | Historical Pattern | Output |
|---|---|---|
| 0–1000 m | Little comparable evidence | Low / informational |
| 1000–2000 m | Rare events | Low |
| 2000–2500 m | Repeated comparable events | Moderate |
| 2500–3000 m | Strong offset-well evidence | High / review |

Where sufficient validated data exists, the system may display calibrated probabilities.

All risk outputs must include:

- Confidence
- Evidence
- Source wells
- Model version
- Data-quality status

---

## 12. RAG / AI Assistant Requirements

The AI assistant should use:

**Question → Intent → Structured Filters → Retrieval → Reranking → Evidence Package → LLM → Citations**

The assistant should prioritize structured event data and use document text as supporting evidence.

It must not invent historical events or recommendations that are not supported by retrieved evidence.

---

## 13. Non-Functional Requirements

### Performance
- Nearby-well search should be fast enough for interactive map use.
- Historical event searches should return usable results without long manual report review.
- Live alerts should be generated with low latency once the stream is available.

### Scalability
The architecture should support future expansion from prototype data to enterprise datasets.

### Reliability
- Failed ingestion jobs must be retryable.
- Source data should remain immutable.
- Predictions should be traceable to model versions.

### Security
- RBAC
- Encryption
- Audit logging
- Source-level access control
- Secure API authentication

### Explainability
Important risk results must show evidence and provenance.

---

## 14. Recommended Product Stack

**Frontend**
- React / Next.js
- Tailwind CSS
- Leaflet / MapLibre / Mapbox

**Backend**
- Python
- FastAPI

**Database**
- PostgreSQL
- PostGIS
- pgvector

**Storage**
- S3-compatible object storage / MinIO

**ML**
- scikit-learn
- XGBoost / LightGBM

**NLP / RAG**
- Sentence Transformers
- pgvector/Qdrant
- Approved LLM/local model

**Processing**
- PyMuPDF
- pdfplumber
- OCR
- lasio
- WITSML/XML parsing

---

## 15. MVP Scope for SIH

### Phase 1
- Open dataset ingestion
- Well normalization
- Map

### Phase 2
- Nearby well search
- Well profile

### Phase 3
- Historical event extraction
- Depth-wise event visualization

### Phase 4
- Well similarity
- Risk profile

### Phase 5
- RAG assistant

### Phase 6
- WITSML/DDR replay
- Simulated real-time alerts

### Phase 7
- Final dashboard
- Evaluation report
- Demo workflow

---

## 16. Success Metrics

Suggested prototype metrics:

- Nearby well retrieval accuracy
- Event extraction precision/recall
- Comparable-well retrieval quality
- Risk-model calibration
- RAG evidence correctness
- Query response time
- Alert precision/recall on historical replay
- Data ingestion success rate

---

## 17. Product Impact

NWIS is intended to:

- Make historical well knowledge easier to access.
- Improve preparation before drilling.
- Highlight repeated historical risks by depth and formation.
- Surface preventive practices earlier.
- Reduce manual report-review effort.
- Support faster engineering analysis.
- Provide a path from historical intelligence to live early-warning analytics.

The system should be described as enabling earlier identification and contextualization of historically observed risks; it does not guarantee prevention of incidents or losses.

---

## 18. USP

**“Institutional memory for drilling — from scattered historical reports to location-aware, depth-aware and evidence-backed drilling intelligence.”**
