import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import folium
from streamlit_folium import st_folium
import time
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="NWIS | Nearby Wells Intelligence System — Pan India",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark Industrial Operations Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #0B0F19;
        color: #F1F5F9;
    }

    .header-banner {
        background: linear-gradient(90deg, #0F172A 0%, #1E293B 50%, #0F172A 100%);
        border: 1px solid #334155;
        border-left: 6px solid #F59E0B;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
    .header-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #F8FAFC;
        margin: 0;
    }
    .header-sub {
        font-size: 1.0rem;
        color: #94A3B8;
        margin-top: 6px;
    }

    .section-box {
        background: #111827;
        border: 1px solid #1F2937;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.25);
    }
    .section-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 2px solid #374151;
        padding-bottom: 10px;
    }

    .card-kpi {
        background: #1F2937;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 16px 20px;
        border-left: 4px solid #F59E0B;
    }
    .card-kpi-val {
        font-size: 2.0rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.1;
    }
    .card-kpi-lbl {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #94A3B8;
        letter-spacing: 0.5px;
    }

    .hazard-card-critical {
        border-left: 5px solid #EF4444 !important;
        background: #1E1B18;
        border: 1px solid #7F1D1D;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .hazard-card-warning {
        border-left: 5px solid #F59E0B !important;
        background: #1E1B18;
        border: 1px solid #78350F;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .hazard-card-safe {
        border-left: 5px solid #10B981 !important;
        background: #064E3B20;
        border: 1px solid #065F46;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }

    .doc-evidence {
        background-color: #FFFBEB;
        color: #78350F;
        border: 1px solid #FDE68A;
        font-family: 'Courier New', Courier, monospace;
        padding: 12px 16px;
        border-radius: 6px;
        font-size: 0.88rem;
        margin-top: 8px;
    }

    .step-badge {
        background: #F59E0B;
        color: #000;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 50%;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Direct Backend Service Imports
from backend.app.db.database import SessionLocal
from backend.app.db.seed_data import seed_database
from backend.app.services.spatial_service import SpatialService
from backend.app.services.risk_service import RiskService
from backend.app.services.recommendation_service import RecommendationService
from backend.app.services.rag_service import DrillingRAGAssistant
from backend.app.ml.anomaly_detector import anomaly_detector
from backend.app.db.models import Well, DrillingTelemetry

# Auto-seed Pan-India DB if needed
seed_database()

# District Centers Reference Dictionary for Dynamic Map Positioning
DISTRICT_CENTERS = {
    "Madhya Pradesh": {
        "Damoh": (23.8323, 79.4422),
        "Shahdol": (23.2968, 81.3533),
        "Katni": (23.8343, 80.3957),
        "Jabalpur": (23.1815, 79.9864)
    },
    "Assam": {
        "Tinsukia": (27.4922, 95.3558),
        "Dibrugarh": (27.4728, 94.9120),
        "Sivasagar": (26.9826, 94.6425)
    },
    "Gujarat": {
        "Bharuch": (21.7051, 72.9959),
        "Gandhinagar": (23.2156, 72.6369)
    },
    "Rajasthan": {
        "Barmer": (25.7521, 71.3967),
        "Jaisalmer": (26.9157, 70.9083)
    },
    "Andhra Pradesh": {
        "East Godavari": (16.9891, 82.2475)
    },
    "West Bengal": {
        "North 24 Parganas": (22.7210, 88.4820)
    },
    "Tripura": {
        "West Tripura": (23.8315, 91.2868)
    }
}

# Session State Initialization
if "show_input_panel" not in st.session_state:
    st.session_state.show_input_panel = True
if "marked_lat" not in st.session_state:
    st.session_state.marked_lat = 23.8420
if "marked_lon" not in st.session_state:
    st.session_state.marked_lon = 79.4510
if "planned_depth" not in st.session_state:
    st.session_state.planned_depth = 3800.0
if "search_radius" not in st.session_state:
    st.session_state.search_radius = 45.0
if "selected_state" not in st.session_state:
    st.session_state.selected_state = "Madhya Pradesh"
if "selected_district" not in st.session_state:
    st.session_state.selected_district = "Damoh"
if "selected_soil" not in st.session_state:
    st.session_state.selected_soil = "Vindhyan Rohtas Limestone & Bhander Sandstone (Madhya Pradesh)"
if "analysis_triggered" not in st.session_state:
    st.session_state.analysis_triggered = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Welcome to NWIS Decision Support. I can provide historical intelligence on offset wells, mud losses, kicks, and preventive practices across India."}
    ]
if "cockpit_frame_idx" not in st.session_state:
    st.session_state.cockpit_frame_idx = 0

# Variables always guaranteed in global scope
planned_depth = float(st.session_state.planned_depth)
search_radius = float(st.session_state.search_radius)
selected_state = str(st.session_state.selected_state)
selected_district = str(st.session_state.selected_district)

# Top Header
st.markdown("""
<div class="header-banner">
    <div class="header-title">🛢️ Nearby Wells Intelligence System (NWIS)</div>
    <div class="header-sub">Oil India Limited — AI Decision-Support & Pan-India Offset Well Institutional Memory</div>
</div>
""", unsafe_allow_html=True)

# Top Bar Toggle Button
col_tgl1, col_tgl2 = st.columns([1, 4])
with col_tgl1:
    if st.button("🎯 Input Your Search Details", use_container_width=True):
        st.session_state.show_input_panel = not st.session_state.show_input_panel

with col_tgl2:
    st.caption("👈 Click to toggle the location input wizard. Follow steps: State → District → Click Map to Pin Point → Soil & Depth → Run Analysis.")

# -----------------------------------------------------------------------------
# STEP-BY-STEP GUIDED SEARCH INPUT PANEL
# -----------------------------------------------------------------------------
if st.session_state.show_input_panel:
    with st.container():
        st.markdown("""
        <div class="section-box" style="border-left: 6px solid #F59E0B;">
            <div class="section-title">
                <span class="step-badge">1</span> Input Your Search Details (Guided Workflow)
            </div>
        """, unsafe_allow_html=True)

        db = SessionLocal()
        available_states = list(DISTRICT_CENTERS.keys())
        db.close()

        col_st, col_dst = st.columns(2)
        with col_st:
            selected_state = st.selectbox(
                "Step 1: Select State in India:",
                available_states,
                index=0,
                key="sel_state"
            )

        # Dynamic District Cascading
        available_districts = list(DISTRICT_CENTERS.get(selected_state, {}).keys())
        with col_dst:
            selected_district = st.selectbox(
                f"Step 2: Select District in {selected_state}:",
                available_districts,
                index=0,
                key="sel_district"
            )

        # Update default center when district changes
        default_center = DISTRICT_CENTERS[selected_state][selected_district]
        
        st.markdown(f"#### Step 3: Interactive District Map — Click on the map to pin your exact proposed drilling location:")
        st.caption(f"Map is automatically centered on **{selected_district}, {selected_state}**. Click anywhere on the map to place a pin marker.")

        # Folium interactive map for clicking
        map_center = [st.session_state.marked_lat, st.session_state.marked_lon]
        
        # If user changed district and current marked_lat is far, re-center on district
        dist_to_center = ((st.session_state.marked_lat - default_center[0])**2 + (st.session_state.marked_lon - default_center[1])**2)**0.5
        if dist_to_center > 1.5:
            st.session_state.marked_lat = default_center[0]
            st.session_state.marked_lon = default_center[1]
            map_center = default_center

        f_map = folium.Map(
            location=map_center,
            zoom_start=11,
            tiles="OpenStreetMap"
        )
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri World Imagery',
            name='Satellite View'
        ).add_to(f_map)

        # Marker at the current pinned location
        folium.Marker(
            [st.session_state.marked_lat, st.session_state.marked_lon],
            tooltip="★ Pinned Proposed Location",
            popup=f"Proposed Well Point<br>Lat: {st.session_state.marked_lat:.4f}<br>Lon: {st.session_state.marked_lon:.4f}",
            icon=folium.Icon(color="red", icon="flag")
        ).add_to(f_map)

        folium.LayerControl().add_to(f_map)

        # Interactive click handler
        map_output = st_folium(f_map, width="100%", height=380, key="picker_map")

        if map_output and map_output.get("last_clicked"):
            clicked = map_output["last_clicked"]
            st.session_state.marked_lat = round(clicked["lat"], 4)
            st.session_state.marked_lon = round(clicked["lng"], 4)

        col_coord1, col_coord2, col_btn_done = st.columns([1.5, 1.5, 1])
        with col_coord1:
            st.info(f"📍 **Pinned Latitude:** `{st.session_state.marked_lat:.4f}° N`")
        with col_coord2:
            st.info(f"📍 **Pinned Longitude:** `{st.session_state.marked_lon:.4f}° E`")
        with col_btn_done:
            st.success("✅ Point Marked & Locked")

        st.markdown("---")

        # Step 4: Soil / Formation Type & Depth / Radius
        col_soil, col_dpth, col_rad = st.columns(3)
        with col_soil:
            soil_options = [
                "Vindhyan Rohtas Limestone & Bhander Sandstone (Madhya Pradesh)",
                "Sirbu Laminated Swelling Shale (Madhya Pradesh)",
                "Sohagpur Coal Cleats / CBM Sequence (Madhya Pradesh)",
                "Tipam Porous Sandstone (Upper Assam)",
                "Barail Coal-Shale High Pressure Gas (Upper Assam)",
                "Kopili Splintery Marine Shale (Upper Assam)",
                "Cambay Organic-rich Fissile Shale (Gujarat)",
                "Ankleshwar Deltaic Sandstone (Gujarat)",
                "Jaisalmer Karstic Limestone (Rajasthan)",
                "Alluvial Sands & Surface Gravel"
            ]
            sel_soil = st.selectbox("Step 4: Soil / Geological Formation Type:", soil_options, index=0 if selected_state == "Madhya Pradesh" else 3)
            st.session_state.selected_soil = sel_soil

        with col_dpth:
            in_depth = st.number_input("Step 5: Planned Total Depth (m MD):", min_value=800.0, max_value=5500.0, value=float(st.session_state.planned_depth), step=100.0)
            st.session_state.planned_depth = in_depth
            planned_depth = in_depth

        with col_rad:
            in_rad = st.slider("Step 6: Offset Search Radius (km):", min_value=5.0, max_value=120.0, value=float(st.session_state.search_radius), step=5.0)
            st.session_state.search_radius = in_rad
            search_radius = in_rad

        st.session_state.selected_state = selected_state
        st.session_state.selected_district = selected_district

        st.markdown("###")
        if st.button("🚀 Run Nearby Wells Intelligence & Risk Analysis", type="primary", use_container_width=True):
            st.session_state.analysis_triggered = True
            st.session_state.show_input_panel = False
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MAIN ANALYSIS RESULTS DASHBOARD (SECTIONS 1 TO 6)
# -----------------------------------------------------------------------------
db = SessionLocal()
nearby_wells = SpatialService.get_nearby_wells(
    db=db,
    latitude=st.session_state.marked_lat,
    longitude=st.session_state.marked_lon,
    radius_km=search_radius
)

risk_profile = RiskService.generate_depth_risk_profile(
    db=db,
    target_lat=st.session_state.marked_lat,
    target_lon=st.session_state.marked_lon,
    planned_depth=planned_depth,
    interval_step_m=500.0,
    search_radius_km=search_radius
)

candidates = RiskService.compare_candidate_locations(
    db=db,
    base_lat=st.session_state.marked_lat,
    base_lon=st.session_state.marked_lon,
    planned_depth=planned_depth,
    radius_km=search_radius
)

hc_evidence = RiskService.get_hydrocarbon_evidence(
    db=db,
    target_lat=st.session_state.marked_lat,
    target_lon=st.session_state.marked_lon,
    radius_km=search_radius
)
db.close()

# KPI Metric Row
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
    <div class="card-kpi">
        <div class="card-kpi-lbl">Offset Wells Found</div>
        <div class="card-kpi-val">{len(nearby_wells)}</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    nearest_text = f"{nearby_wells[0]['distance_km']} km" if nearby_wells else "None"
    st.markdown(f"""
    <div class="card-kpi">
        <div class="card-kpi-lbl">Closest Offset Distance</div>
        <div class="card-kpi-val">{nearest_text}</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    tot_events = sum(w["historical_events_count"] for w in nearby_wells)
    st.markdown(f"""
    <div class="card-kpi">
        <div class="card-kpi-lbl">Recorded Incidents in Radius</div>
        <div class="card-kpi-val" style="color: {'#EF4444' if tot_events > 0 else '#10B981'};">{tot_events}</div>
    </div>
    """, unsafe_allow_html=True)
with k4:
    ovr_risk = risk_profile["overall_summary"]["overall_risk_level"]
    risk_col = "#EF4444" if "HIGH" in ovr_risk else ("#F59E0B" if "MODERATE" in ovr_risk else "#10B981")
    st.markdown(f"""
    <div class="card-kpi" style="border-left-color: {risk_col};">
        <div class="card-kpi-lbl">Overall Prospect Hazard</div>
        <div class="card-kpi-val" style="color: {risk_col}; font-size: 1.6rem;">{ovr_risk}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("###")

# =============================================================================
# SECTION 1: NEARBY WELLS DISCOVERED (आस-पास खुदे हुए कुएं)
# =============================================================================
st.markdown("""
<div class="section-box">
    <div class="section-title">
        <span>🗺️</span> SECTION 1: Nearby Wells Discovered (आस-पास खुदे हुए कुएं)
    </div>
""", unsafe_allow_html=True)

col_sec1_map, col_sec1_tbl = st.columns([1.1, 0.9])

with col_sec1_map:
    # Build Map with Proposed Point & Nearby Wells
    res_map = folium.Map(
        location=[st.session_state.marked_lat, st.session_state.marked_lon],
        zoom_start=10,
        tiles="CartoDB dark_matter"
    )

    # Search Radius Ring
    folium.Circle(
        radius=search_radius * 1000.0,
        location=[st.session_state.marked_lat, st.session_state.marked_lon],
        color="#F59E0B",
        fill=True,
        fill_color="#F59E0B",
        fill_opacity=0.08,
        weight=2
    ).add_to(res_map)

    # Proposed Location Marker
    folium.Marker(
        [st.session_state.marked_lat, st.session_state.marked_lon],
        tooltip="★ Proposed Drilling Location",
        popup=f"<b>PROPOSED LOCATION</b><br>Target Depth: {planned_depth}m<br>Radius: {search_radius}km",
        icon=folium.Icon(color="orange", icon="star")
    ).add_to(res_map)

    # Offset Wells
    for w in nearby_wells:
        inc = w["historical_events_count"]
        m_color = "red" if inc > 0 else "blue"
        popup_txt = f"""
        <div style="font-family: sans-serif; font-size: 12px; width: 220px;">
            <b>{w['name']}</b> ({w['field']})<br>
            <b>Operator:</b> {w['operator']}<br>
            <b>Distance:</b> {w['distance_km']} km ({w['direction']})<br>
            <b>Total Depth:</b> {w['total_depth']} m<br>
            <b>Incidents:</b> <span style="color: {'red' if inc > 0 else 'green'}; font-weight: bold;">{inc}</span>
        </div>
        """
        folium.Marker(
            [w["latitude"], w["longitude"]],
            tooltip=f"{w['name']} ({w['distance_km']} km)",
            popup=folium.Popup(popup_txt, max_width=250),
            icon=folium.Icon(color=m_color, icon="tint")
        ).add_to(res_map)

    st_folium(res_map, width="100%", height=420, key="results_map")

with col_sec1_tbl:
    if nearby_wells:
        st.markdown("#### 📋 Offset Wells Summary Table:")
        df_display = pd.DataFrame([
            {
                "Well Name": w["name"],
                "Operator": w["operator"],
                "Distance": f"{w['distance_km']} km",
                "Direction": f"{w['direction']} ({w['bearing_degrees']}°)",
                "Total Depth": f"{w['total_depth']} m",
                "Historical Incidents": f"⚠️ {w['historical_events_count']}" if w['historical_events_count'] > 0 else "None"
            }
            for w in nearby_wells
        ])
        st.dataframe(df_display, use_container_width=True, hide_index=True)

        st.markdown("#### 🔍 Inspect Historical Well Dossier:")
        inspect_id = st.selectbox("Select Offset Well:", [w["well_id"] for w in nearby_wells], key="sel_insp")
        db = SessionLocal()
        insp_well_obj = db.query(Well).filter(Well.well_id == inspect_id).first()
        if insp_well_obj:
            with st.expander(f"📖 {insp_well_obj.name} Profile & Formation Tops", expanded=False):
                st.write(f"**Operator:** {insp_well_obj.operator} | **Total Depth:** {insp_well_obj.total_depth}m | **Status:** {insp_well_obj.status}")
                forms = [{"Formation": f.formation_name, "Top": f"{f.top_depth_md}m", "Base": f"{f.base_depth_md}m", "Lithology": f.lithology} for f in insp_well_obj.formations]
                st.table(pd.DataFrame(forms))
        db.close()
    else:
        st.warning(f"No historical wells found within {search_radius} km of the marked point. Try increasing the search radius.")

st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# SECTION 2: EXPECTED INCIDENTS & HAZARD FORECAST (जो घटनाएं हो सकती हैं)
# =============================================================================
st.markdown("""
<div class="section-box">
    <div class="section-title">
        <span>⚠️</span> SECTION 2: Expected Incidents & Hazard Forecast (जो घटनाएं हो सकती हैं)
    </div>
""", unsafe_allow_html=True)

intervals = risk_profile["depth_intervals"]

col_chart, col_haz_cards = st.columns([1, 1.2])

with col_chart:
    st.markdown("#### 📊 Multi-Hazard Likelihood vs. Depth:")
    chart_depths = [inv["interval_label"] for inv in intervals]
    mud_loss_probs = [inv["ml_probabilities"].get("Mud Loss", 0.0) for inv in intervals]
    kick_probs = [inv["ml_probabilities"].get("Gas Kick", 0.0) for inv in intervals]
    stuck_probs = [inv["ml_probabilities"].get("Stuck Pipe", 0.0) for inv in intervals]

    fig_haz = go.Figure()
    fig_haz.add_trace(go.Bar(name='Mud Loss Likelihood', x=chart_depths, y=mud_loss_probs, marker_color='#38BDF8'))
    fig_haz.add_trace(go.Bar(name='Gas Kick Likelihood', x=chart_depths, y=kick_probs, marker_color='#EF4444'))
    fig_haz.add_trace(go.Bar(name='Stuck Pipe Likelihood', x=chart_depths, y=stuck_probs, marker_color='#F59E0B'))

    fig_haz.update_layout(
        barmode='group',
        paper_bgcolor='#111827',
        plot_bgcolor='#1F2937',
        font=dict(color='#94A3B8'),
        yaxis=dict(title='Probability (0 to 1.0)', range=[0, 1.0]),
        height=380,
        margin=dict(l=40, r=20, b=30, t=30)
    )
    st.plotly_chart(fig_haz, use_container_width=True)

with col_haz_cards:
    st.markdown("#### 🚨 Depth-Wise Hazard Intervals:")
    for inv in intervals:
        risk_lvl = inv["risk_level"]
        c_class = "hazard-card-critical" if "HIGH" in risk_lvl else ("hazard-card-warning" if "MODERATE" in risk_lvl else "hazard-card-safe")
        badge_dot = "🔴 HIGH HAZARD" if "HIGH" in risk_lvl else ("🟡 MODERATE" if "MODERATE" in risk_lvl else "🟢 LOW")

        st.markdown(f"""
        <div class="{c_class}">
            <div style="display: flex; justify-content: space-between;">
                <b>{badge_dot}: Depth {inv['interval_label']}</b>
                <span>Risk Score: <b>{inv['risk_score']}</b></span>
            </div>
            <div style="margin-top: 4px; color: #E2E8F0;">
                <b>Formation:</b> {inv['formation_name']} ({inv['lithology']})
            </div>
        </div>
        """, unsafe_allow_html=True)

        if inv["historical_events"]:
            for ev in inv["historical_events"]:
                st.caption(f"• **Offset Incident in {ev['well_name']} ({ev['event_type']}):** {ev['description']}")

st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# SECTION 3: EVIDENCE-BACKED PREVENTIVE RECOMMENDATIONS (सफल प्रिवेंटिव उपाय)
# =============================================================================
st.markdown("""
<div class="section-box">
    <div class="section-title">
        <span>🛡️</span> SECTION 3: Evidence-Backed Preventive Recommendations (सफल प्रिवेंटिव उपाय)
    </div>
""", unsafe_allow_html=True)

st.markdown("Based on historical incident resolutions in the nearby offset wells, here are the verified preventive SOPs and mitigations:")

found_mitigations = False
for inv in intervals:
    if inv["preventive_recommendations"]:
        found_mitigations = True
        with st.expander(f"🛡️ SOPs for Depth {inv['interval_label']} ({inv['formation_name']})", expanded=True):
            for rec in inv["preventive_recommendations"]:
                st.info(f"**Hazard: {rec['event_type']}**\n\n**Action Taken in Offset Well:** {rec['action_taken']}\n\n**Recommended Preventive Practice:** {rec['recommended_practice']}\n\n*Reference Authority:* `{rec['source_reference']}`")

if not found_mitigations:
    st.info("No high-severity incidents recorded in nearby wells requiring specialized LCM pills or kill methods for this depth.")

st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# SECTION 4: CANDIDATE LOCATIONS & HYDROCARBONS (PRD FR-14 & FR-15)
# =============================================================================
st.markdown("""
<div class="section-box">
    <div class="section-title">
        <span>🧭</span> SECTION 4: Alternative Candidate Locations & Hydrocarbon Shows (FR-14 & FR-15)
    </div>
""", unsafe_allow_html=True)

col_alt_pads, col_hc_shows = st.columns(2)

with col_alt_pads:
    st.markdown("#### 🎯 Alternative Surface Pad Risk Comparison (FR-14)")
    df_cands = pd.DataFrame([
        {
            "Pad ID": c["candidate_id"],
            "Location Name": c["name"],
            "Coordinates": f"{c['latitude']}°N, {c['longitude']}°E",
            "Avg Risk Score": c["average_risk_score"],
            "High-Risk Zones": f"{c['high_risk_intervals']} Intervals",
            "Recommendation": c["geological_recommendation"]
        }
        for c in candidates
    ])
    st.dataframe(df_cands, use_container_width=True, hide_index=True)
    st.success(f"💡 **AI Pad Optimizer:** Pad **{candidates[0]['name']}** offers the lowest historical incident exposure.")

with col_hc_shows:
    st.markdown("#### 🛢️ Historical Hydrocarbon Shows & Pay Zones (FR-15)")
    if hc_evidence:
        for hc in hc_evidence[:3]:
            st.markdown(f"""
            <div style="background: #1E293B; border-left: 4px solid #10B981; padding: 12px; border-radius: 6px; margin-bottom: 8px;">
                <b>{hc['well_name']}</b> ({hc['distance_km']} km {hc['direction']})<br>
                <b>Pay Zone:</b> {hc['depth_interval']} ({hc['formation']})<br>
                <b>Fluid Type:</b> {hc['fluid_type']} | <b>Net Pay:</b> {hc['net_pay_m']}m<br>
                <b>DST Test Flow:</b> <code>{hc['dst_flow_rate']}</code>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No open hydrocarbon test records found in the immediate search radius.")

st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# SECTION 5: AI DRILLING ASSISTANT (RAG) WITH SOURCE PROVENANCE
# =============================================================================
st.markdown("""
<div class="section-box">
    <div class="section-title">
        <span>🤖</span> SECTION 5: AI Drilling Assistant (Zero-Hallucination RAG)
    </div>
""", unsafe_allow_html=True)

st.markdown("**💡 Quick Question Prompts:**")
qp1, qp2, qp3 = st.columns(3)
with qp1:
    if st.button("💧 Mud losses in Limestone / Sandstone"):
        st.session_state.pending_chat = "Show nearby wells that experienced mud loss in Limestone or Sandstone"
with qp2:
    if st.button("🔥 Gas kicks in deep formations"):
        st.session_state.pending_chat = "What gas kicks happened in nearby wells and what kill method was used?"
with qp3:
    if st.button("🔒 Stuck pipe and freeing actions"):
        st.session_state.pending_chat = "Show stuck pipe incidents in shale and the pipe freeing action taken"

user_chat = st.chat_input("Ask any drilling question about nearby offset wells, hazards, mud weights...")

if "pending_chat" in st.session_state and st.session_state.pending_chat:
    user_chat = st.session_state.pending_chat
    st.session_state.pending_chat = None

if user_chat:
    st.session_state.chat_history.append({"role": "user", "content": user_chat})
    db = SessionLocal()
    rag_ans = DrillingRAGAssistant.answer_query(db=db, user_query=user_chat)
    db.close()

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": rag_ans["answer"],
        "citations": rag_ans.get("citations", [])
    })

for m in st.session_state.chat_history:
    if m["role"] == "user":
        with st.chat_message("user"):
            st.write(m["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(m["content"])
            if "citations" in m and m["citations"]:
                st.markdown("##### 📄 Verified Source Document Provenance:")
                for c in m["citations"]:
                    st.markdown(f"""
                    <div class="doc-evidence">
                        <b>DOCUMENT:</b> {c['source_document']} (Page {c['page_number']}) | <b>WELL:</b> {c['well_name']} ({c['field']})<br>
                        <b>EXCERPT:</b> "{c['evidence_snippet']}"
                    </div>
                    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# SECTION 6: REAL-TIME eRTMAC LIVE DRILLING COCKPIT (SIMULATOR)
# =============================================================================
st.markdown("""
<div class="section-box">
    <div class="section-title">
        <span>⚡</span> SECTION 6: Real-Time eRTMAC / WITSML Drilling Cockpit
    </div>
""", unsafe_allow_html=True)

db = SessionLocal()
telemetry_data = db.query(DrillingTelemetry).filter(DrillingTelemetry.well_id == "OIL-BGJ-01").order_by(DrillingTelemetry.depth_md.asc()).all()
db.close()

if telemetry_data:
    c_btn1, c_btn2, c_sld = st.columns([1, 1, 3])
    with c_btn1:
        if st.button("▶️ Step Next Live Frame"):
            if st.session_state.cockpit_frame_idx < len(telemetry_data) - 1:
                st.session_state.cockpit_frame_idx += 1
    with c_btn2:
        if st.button("🚨 Jump to Kick Event"):
            for i, p in enumerate(telemetry_data):
                if p.depth_md >= 2991.5:
                    st.session_state.cockpit_frame_idx = i
                    break
    with c_sld:
        st.session_state.cockpit_frame_idx = st.slider("Live Replay Stream Frame:", 0, len(telemetry_data)-1, st.session_state.cockpit_frame_idx)

    curr_p = telemetry_data[st.session_state.cockpit_frame_idx]
    
    # Anomaly evaluation
    t_snap = {
        "well_id": curr_p.well_id,
        "depth_md": curr_p.depth_md,
        "wob": curr_p.wob,
        "rpm": curr_p.rpm,
        "torque": curr_p.torque,
        "rop": curr_p.rop,
        "spp": curr_p.spp,
        "flow_in": curr_p.flow_in,
        "mud_weight": curr_p.mud_weight
    }
    alert_obj = anomaly_detector.evaluate_telemetry_point(t_snap)

    if alert_obj:
        st.markdown(f"""
        <div style="background: #7F1D1D; border: 2px solid #EF4444; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
            <h3 style="color: #FEE2E2; margin: 0;">🚨 {alert_obj['severity']}: {alert_obj['hazard_type']}</h3>
            <p style="color: #FECACA; margin: 6px 0;"><b>ALERT:</b> {alert_obj['message']}</p>
            <div style="background: #991B1B; padding: 8px 12px; border-radius: 4px; color: #FFF;">
                <b>Required Action:</b> {alert_obj['recommended_immediate_action']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success(f"✅ Normal Drilling Telemetry at {curr_p.depth_md:.1f} m MD. All parameters within safe operating bounds.")

    # 6 Gauges
    g1, g2, g3, g4, g5, g6 = st.columns(6)
    with g1:
        st.metric("ROP (m/h)", f"{curr_p.rop:.1f}", delta=f"{curr_p.rop - 15.0:.1f}" if curr_p.rop > 20 else None)
    with g2:
        st.metric("SPP (bar)", f"{curr_p.spp:.0f}", delta=f"{curr_p.spp - 185.0:.0f}" if curr_p.spp < 175 else None)
    with g3:
        st.metric("Torque (kNm)", f"{curr_p.torque:.1f}")
    with g4:
        st.metric("WOB (kN)", f"{curr_p.wob:.0f}")
    with g5:
        st.metric("Flow In (gpm)", f"{curr_p.flow_in:.0f}")
    with g6:
        st.metric("Mud Weight (SG)", f"{curr_p.mud_weight:.2f}")

st.markdown("</div>", unsafe_allow_html=True)
