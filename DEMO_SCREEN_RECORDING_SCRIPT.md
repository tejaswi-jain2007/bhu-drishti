# 🎬 3-Minute Prototype Demo Video Script
## 🛢️ भू-DRISHTI: Subsurface Intelligence & Autonomous Well-Control Copilot
### *Oil India Limited — Smart India Hackathon (SIH 2026)*

**Target Video Duration:** 2 Minutes 50 Seconds (Under 3 Minutes)  
**Tone:** High-Energy, Professional, Pitch-Ready, Technical yet Clear  
**Screen Setup:** 1920x1080 Full Screen, Dark/Light Mode, Browser open at `http://localhost:3000`

---

## ⏱️ Video Timeline & Scene Breakdown

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                      3-MINUTE DEMO WALKTHROUGH TIMELINE                     │
└─────────────────────────────────────────────────────────────────────────────┘
  [0:00 - 0:30] ──> Scene 1: Introduction & Executive Dashboard Overview
  [0:30 - 1:15] ──> Scene 2: Geospatial Offset Search & Campaign Configurator
  [1:15 - 2:00] ──> Scene 3: ML Depth-Wise Hazard Risk Engine & Mitigations
  [2:00 - 2:35] ──> Scene 4: Real-Time eRTMAC Telemetry & Early-Warning Alerts
  [2:35 - 3:00] ──> Scene 5: RAG AI Assistant with Citations & Closing Pitch
```

---

## 📽️ Detailed Scene-by-Scene Script

### Scene 1: Introduction & Executive Dashboard (0:00 – 0:30)

**💻 On-Screen Action:**
- Screen shows the main landing page of **भू-DRISHTI** (`http://localhost:3000`).
- Cursor hovers over the official **भू-DRISHTI** logo, the top header badge, and the KPI stat strip showing 77 wells, 8 sedimentary basins, and real-time ML risk indicators.

**🗣️ Spoken Voiceover:**
> *"This is our dashboard of **भू-DRISHTI** — India’s indigenous Subsurface Intelligence and Autonomous Well-Control Copilot, engineered for **Oil India Limited** under SIH 2026.*
>
> *Every year, drilling operations face millions of dollars in Non-Productive Time due to unforeseen downhole hazards like mud losses, gas kicks, and stuck pipe. **भू-DRISHTI** solves this by converting decades of historical WCRs, DDRs, and daily rig telemetry into real-time, depth-indexed actionable intelligence."*

---

### Scene 2: Geospatial Offset Discovery & Campaign Configurator (0:30 – 1:15)

**💻 On-Screen Action:**
- Click on **State/District Selector** -> Select **Assam** -> **Dibrugarh / Tinsukia (Upper Assam Shelf)**.
- Adjust the **Search Radius Slider** to `25 km` and set Planned Target Depth to `3,800m`.
- Click **"Run Geospatial Search"**. The interactive map instantly updates with satellite tiles, showing offset wells (NHR-1, NHK-08, Moran, Digboi) with exact geodetic distance and bearings.

**🗣️ Spoken Voiceover:**
> *"Let’s simulate planning a new development well in the Upper Assam Shelf. We select Dibrugarh district, set a target depth of 3,800 meters, and define a 25-kilometer search radius.*
>
> *Instantly, our PostGIS geodetic engine discovers all historical offset wells. We can inspect well trajectories, drilling years, target formation tops like **Barail Coal-Shale** and **Tipam Sandstone**, and see exact spatial proximity."*

---

### Scene 3: ML Depth-Wise Hazard Risk Engine & Past Mitigations (1:15 – 2:00)

**💻 On-Screen Action:**
- Click on **"Depth-Wise Risk Profile"** tab. Scroll through the 50m interval risk chart.
- Highlight the **High Risk Band** (Red indicator at 2,800m – 3,100m for Mud Loss & Overpressure Kick).
- Click on **"Preventive Recommendations"** panel. Expand the source evidence citation showing offset well `OIL-NHK-08` WCR document page 42.

**🗣️ Spoken Voiceover:**
> *"Now, our Machine Learning risk engine analyzes lithological similarity and historical event frequency to generate a depth-indexed hazard profile.*
>
> *Notice here at 2,850 meters in the Barail formation: the model flags an **84% High Risk** of severe mud loss and pressure kick influx. But **भू-DRISHTI** doesn’t just flag risks — it gives solutions.*
>
> *Here in the Recommendations Panel, it surfaces exact past engineering playbooks: pumping a 40-barrel LCM Mica pill at 1.34 SG mud weight, verified directly from offset well NHK-08’s completion report."*

---

### Scene 4: Real-Time eRTMAC Rig Monitor & Anomaly Detection (2:00 – 2:35)

**💻 On-Screen Action:**
- Click on **"Real-Time Monitor"** tab.
- Click **"Start Live WITSML Stream Replay"**. The live telemetry charts (ROP, WOB, RPM, Standpipe Pressure, Torque) begin updating dynamically at 1 Hz.
- Anomaly detector triggers a pulsing red alert modal: `CRITICAL: Overpressure Kick Influx Detected at 3,240m MD`.

**🗣️ Spoken Voiceover:**
> *"Once drilling begins, **भू-DRISHTI** connects directly to live rig telemetry via **WITSML 1.4.1.1** and **eRTMAC** streams.*
>
> *As sensor data streams in at 1 Hertz, our Isolation Forest anomaly detector compares live drill string torque and standpipe pressure against historical signatures. The moment a pressure influx signature is detected, it triggers instant early-warning alerts before a catastrophic blowout can occur."*

---

### Scene 5: RAG AI Assistant & Closing Pitch (2:35 – 3:00)

**💻 On-Screen Action:**
- Open **AI Assistant** chat drawer. Type: *"What mud weight cured mud losses in Barail at 2800m?"*
- Watch the instant response stream with green verified badge and direct source page citation (`WCR-NHK-08, Page 42`).
- Pan back to full dashboard with **Oil India Limited** & **भू-DRISHTI** branding.

**🗣️ Spoken Voiceover:**
> *"Finally, engineers can chat directly with 40 years of institutional memory using our zero-hallucination RAG Assistant, getting instant, source-cited answers.*
>
> ***भू-DRISHTI** transforms passive historical archives into proactive operational safety. Safer wells, lower NPT, and stronger technology for **Oil India Limited**. Thank you!"*

---

## 📌 Checklist Before Hitting Record
- [x] Backend running on `http://localhost:8000`
- [x] Frontend running on `http://localhost:3000`
- [x] Clear browser address bar / use Chrome App mode
- [x] Mic audio tested & noise cancellation active
- [x] Cursor highlight / click effects enabled in OBS / Screen recorder
