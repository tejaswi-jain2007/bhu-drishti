# 🛢️ Nearby Wells Intelligence System (NWIS)
## Complete Project Guide: Problem Statement, Purpose & Solution Architecture
### *Oil India Limited (OIL) — Smart India Hackathon (SIH 2026)*

---

## 📌 1. Project Kya Hai? (What is this Project?)

**NWIS (Nearby Wells Intelligence System)** ek **AI/ML-powered Decision Support & Institutional Memory System** hai, jo **Oil India Limited (OIL)** ke liye develop kiya gaya hai. 

Jab bhi Oil India kisi nayi jagah par tel ya gas ka kuan (**New Drilling Well**) khodne ka plan banati hai, toh NWIS purane saare aas-paas ke kuon (**Offset / Nearby Historical Wells**) ke hazaron panno ke drilling records (WCRs, Daily Drilling Reports - DDRs, Mud Logs, Well Trajectories, Geological Formations) ko analyse karke **pehle se bata deta hai ki kis depth par kya khatra (Risk) aa sakta hai aur use kaise roka jaye.**

### 🎯 Ek Line Me Summary:
> **"Past Drilling Experience se Seekh kar Future Wells ko Safely, Fast aur Cost-Effectively Drill karne wala Intelligent AI Co-Pilot."**

---

## ⚠️ 2. Problem Statement Kya Hai? Aur Ye Kyu Chahiye? (Why NWIS?)

### 🚨 Real-World Industry Problem:
Oil & Gas drilling duniya ke sabse expensive aur high-risk engineering operations me se ek hai:
1. **Huge Cost of Drilling:** Ek offshore ya deep onshore drilling rig ka per-day operational cost **₹15 Lakh se ₹1.5 Crore ($20,000 - $150,000 / day)** tak hota hai.
2. **NPT (Non-Productive Time) Losses:** Jab drill pipe phans jati hai (**Stuck Pipe**), drilling fluid gayab ho jata hai (**Mud Loss**), ya high-pressure gas achanak leak ho jati hai (**Gas Kick / Blowout hazard**), toh drilling ruk jati hai. Isse har saal Oil companies ko **crores of rupees** ka loss hota hai.
3. **"Dark Data" & Disconnected Records:** 
   - 30-40 saal purane Well Completion Reports (WCRs) aur daily reports PDF files, paper folders, aur alag-alag databases me band pade hain.
   - Naya well plan karte waqt engineers ke paas time nahi hota ki wo 20 purane reports ke 5,000 pages manually padhein.
4. **Lack of Real-Time Warning:** Jab live drilling chal rahi hoti hai, toh field engineers ko ye pata nahi hota ki 3 saal pehle 1.5 km door wale well me isi exact depth aur formation par kya problem aayi thi.

```text
❌ TRADITIONAL APPROACH:
[New Well Plan] ──> [Scattered 1000s of PDF Reports] ──> [Manual Search (Days)] ──> [Drilling "Blind"] ──> [Stuck Pipe / Mud Loss / High NPT]

✅ NWIS INTELLIGENT APPROACH:
[New Well Coordinates + Depth] ──> [NWIS AI Engine] ──> [Instant Offset Correlation + Depth-wise Risk Profile + Past Mitigations + Real-time Alerting]
```

---

## 💡 3. Kaise Solve Ho Raha Hai? (How NWIS Solves This Problem)

NWIS is problem ko **6 Core Technological Modules** ke through solve karta hai:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           NWIS SOLUTION WORKFLOW                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
  1. GEOSPATIAL SEARCH                ▼
     Pinpoint proposed location ──> Radius Search (1-50 km) ──> Find Offset Wells
                                      │
  2. STRATIGRAPHIC CORRELATION        ▼
     Align Measured Depth (MD), TVD, Formations (Barail, Tipam, Kopili, etc.)
                                      │
  3. ML HAZARD PREDICTION             ▼
     Predict probabilities for Mud Loss, Kicks, Stuck Pipe at 50m intervals
                                      │
  4. HISTORICAL RECOMMENDATIONS       ▼
     Surface exact mud weights, ECD limits, LCM pills used successfully in past
                                      │
  5. REAL-TIME eRTMAC MONITORING      ▼
     Stream live rig data (ROP, WOB, RPM, Torque, SPP) & trigger early warnings
                                      │
  6. CONVERSATIONAL RAG AI            ▼
     Ask natural language questions & get zero-hallucination answers with citations
```

---

### 🔹 Module 1: Geospatial Discovery & Well Campaign Configurator
- **What it does:** User map par click karke ya Coordinates (Lat/Lon), State (Assam, Rajasthan, Gujarat), District aur Target Depth dalta hai.
- **How it solves:** PostGIS aur Haversine algorithms se configurable radius (e.g. 10 km, 25 km) ke andar saare historical wells ko extract karta hai, unka exact distance, direction (bearing), operator aur drilling year dikhata hai.

---

### 🔹 Module 2: Cross-Well Stratigraphic & Depth Alignment
- **What it does:** Alag-alag wells ki depth ko compare karna tricky hota hai kyunki zameen ke niche formations tilted ya wavy hoti hain.
- **How it solves:** NWIS **Measured Depth (MD)**, **True Vertical Depth (TVD)**, aur **Subsea Depth (TVDSS)** ko normalize karta hai aur formation tops (jaise *Barail Coal-Shale, Tipam Sandstone, Kopili Formation*) ko visually aur mathematically align karta hai.

---

### 🔹 Module 3: Machine Learning Depth-Wise Risk Engine
- **What it does:** Planned well ke har 50 meter ke interval (e.g., 2000m-2050m, 2050m-2100m...) par forecast karta hai ki kaun sa hazard hone ka kitna chance hai.
- **Hazard Categories Covered:**
  1. 🔴 **Mud Loss** (Fluid circulation loss in fractured rock)
  2. 🔴 **Gas/Water Kick** (Dangerous influx of formation pressure)
  3. 🔴 **Stuck Pipe** (Mechanical or differential pipe sticking)
  4. 🔴 **Fishing Job** (Equipment broken downhole)
  5. 🔴 **Pressure Anomaly** (Overpressure / Underpressure zones)
  6. 🔴 **Torque & Drag Spikes** (Hole instability / tight hole)
- **Mathematical Logic:**
  - Historical event frequency +
  - Multi-well similarity weighting (distance + geological match + depth variance) +
  - Calibrated ML models (XGBoost / Random Forest) = **Normalized Risk Index (0.0 to 1.0)** with Low, Moderate, High, Critical bands.

---

### 🔹 Module 4: Evidence-Backed Recommendations & Playbooks
- **What it does:** Sirf risk batana kaafi nahi hota; engineers ko solution chahiye.
- **How it solves:** Agar system 2800m par *Mud Loss* ka high risk detect karta hai, toh wo offset well (e.g., Well `OIL-NHK-08`) se exact past mitigation nikalta hai:
  > *"At 2820m, 40 bbls of Nutplug + Mica LCM pill was pumped at 1.18 SG mud weight, curing the 80 bbl/hr loss within 2 hours. See WCR Page 42."*

---

### 🔹 Module 5: Real-Time eRTMAC & WITSML Live Monitor
- **What it does:** Real-time operational platform (**eRTMAC**) se live drilling sensors ka data leta hai.
- **Telemetry Monitored (1 Hz to 5 Hz WebSocket):**
  - **ROP** (Rate of Penetration)
  - **WOB** (Weight on Bit)
  - **RPM** (Rotary Table Speed)
  - **Torque** & **SPP** (Standpipe Pressure)
  - **Flow In / Flow Out** & **Mud Weight / ECD**
- **Anomaly Detection:** **Isolation Forest + Trend Deviation Rules** jaise hi live data me abnormal pattern dekhte hain (e.g., SPP drop + Flow Out increase = Kick), instant warning alert trigger hota hai.

---

### 🔹 Module 6: Conversational RAG AI Assistant
- **What it does:** Technical drilling reports me search karne ke liye chat interface deta hai.
- **Zero-Hallucination Guarantee:** 
  - SentenceTransformers + Vector Search + Document Metadata filters use karke pehle actual document chunks extract karta hai.
  - LLM sirf aur sirf retrieved facts ke base par answer deta hai aur har line ke sath **Document Name, Well ID, and Page Number** cite karta hai.

---

## 💻 4. Project Tech Stack & Codebase Structure

| Layer | Technologies Used | What It Does in NWIS |
|---|---|---|
| **Frontend Web UI** | Next.js 16 (React 18), TypeScript, Tailwind CSS, Lucide Icons | Premium drilling operations web dashboard |
| **Mapping Engine** | Leaflet, React-Leaflet, OpenStreetMap Tile Layers | Interactive well location picker & radius visualizer |
| **Desktop GUI** | Python Tkinter / CustomTkinter (`gui/app_gui.py`) | Standalone offline GUI for remote rig sites with low internet |
| **Backend API Gateway** | Python 3.10+, FastAPI, Uvicorn, Pydantic | High-performance Async REST API + WebSockets |
| **Database & GIS** | SQLite3 / PostgreSQL + PostGIS + pgvector | Spatial queries, well metadata, and vector storage |
| **ML & Analytics** | Scikit-learn, XGBoost, Isolation Forest, NumPy, Pandas | Anomaly detection, risk scoring, similarity engine |
| **NLP & RAG** | SentenceTransformers, FAISS/pgvector, PyMuPDF, OCR | Semantic search across historical WCR/DDR PDF documents |
| **Well Log Ingestion** | `lasio`, XML/WITSML parser | Digital log curve (GR, RES, NPHI) & telemetry ingestion |

### 📂 Repository File Structure Overview
```text
SIH-2/
├── NWIS_PRD.md                  # Detailed Product Requirements Document
├── NWIS_TRD.md                  # Detailed Technical Requirements Document
├── NWIS_MASTER_DOCUMENTATION.md # Unified Master Blueprint
├── PROJECT_OVERVIEW_EXPLAINED.md# This comprehensive explanation guide
├── NWIS_PRD.pdf                 # Professional PDF of PRD
├── NWIS_TRD.pdf                 # Professional PDF of TRD
├── NWIS_MASTER_DOCUMENTATION.pdf# Professional PDF of Master Blueprint
├── build_pdf_docs.py            # Automated PDF compilation utility
├── start_all.bat                # 1-Click launcher (Backend + Frontend)
│
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app initialization & CORS
│   │   ├── api/                 # REST routes (wells, risk, assistant, alerts, live)
│   │   ├── ml/                  # ML models (similarity, depth risk, anomaly detector)
│   │   ├── services/            # Core business logic (spatial, correlation, RAG, risk)
│   │   └── ingestion/           # Parsers for PDF, LAS, WITSML, CSV
│
├── frontend/
│   └── src/
│       ├── app/                 # Next.js App router & pages
│       └── components/          # React components (Map, RiskDashboard, AIAssistant, RealTimeMonitor, etc.)
│
├── gui/
│   └── app_gui.py               # Standalone Python Desktop GUI
│
└── data/
    ├── nwis.db                  # SQLite database with normalized well data
    ├── raw/ & processed/        # Historical logs, WCRs, DDRs, Volve & NLOG datasets
    └── models/                  # Serialized ML model weights (.pkl)
```

---

## 🚀 5. How to Run the Project (Step-by-Step)

### Option A: Complete Web Platform (Recommended)
Double click on `start_all.bat` or run in terminal:
```cmd
start_all.bat
```
- **Frontend Dashboard:** Opens automatically at `http://localhost:3000`
- **Backend API Docs (Swagger UI):** Available at `http://localhost:8000/docs`

### Option B: Standalone Desktop GUI (Offline Rig Mode)
Agar internet connection nahi hai ya quick lightweight interface chahiye:
```powershell
python run_gui.py
```

### Option C: Regenerate Documentation PDFs
Kisi bhi time updated PDFs create karne ke liye:
```powershell
python build_pdf_docs.py
```

---

## 🏆 6. Key Advantages & Innovation (SIH 2026 Pitch Points)

1. **True Institutional Memory:** 40 saal ka drilling experience 2 seconds me engineer ke screen par accessible hota hai.
2. **Proactive vs Reactive:** Problem aane ke baad react karne ke badle drill karne se pehle hi risk zones aur mitigations pata chal jati hain.
3. **Rig-Ready Hybrid Architecture:** High-speed web interface ke sath-sath remote offline rig sites ke liye standalone Python desktop app bhi ready hai.
4. **Zero-Hallucination RAG:** Chatbot hawa me baatein nahi karta; har factual statement ke peeche source document ka page number aur well name hota hai.
5. **eRTMAC & WITSML Ready:** Existing Oil India infrastructure ke sath plug-and-play compatibility ke liye WITSML standards implement kiye gaye hain.
