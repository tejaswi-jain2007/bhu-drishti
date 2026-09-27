import random
import datetime
import os
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.db.models import (
    Well, WellTrajectory, Formation, DrillingEvent, Mitigation, DrillingTelemetry
)

def create_tables():
    Base.metadata.create_all(bind=engine)

def seed_database(db: Session = None, force: bool = False):
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    create_tables()

    # If force is False and wells exist, check if MP wells exist; if not, re-seed
    if not force:
        has_mp = db.query(Well).filter(Well.state == "Madhya Pradesh").count() > 0
        if has_mp and db.query(Well).count() >= 25:
            if close_db:
                db.close()
            return

    # Clear existing to ensure clean Pan-India dataset
    db.query(DrillingTelemetry).delete()
    db.query(Mitigation).delete()
    db.query(DrillingEvent).delete()
    db.query(WellTrajectory).delete()
    db.query(Formation).delete()
    db.query(Well).delete()
    db.commit()

    random.seed(42)

    # Comprehensive Pan-India Well Database (Madhya Pradesh, Assam, Gujarat, Rajasthan, AP, West Bengal, Tripura)
    wells_data = [
        # -------------------------------------------------------------
        # 1. MADHYA PRADESH (Vindhyan Basin & CBM Blocks)
        # -------------------------------------------------------------
        {
            "well_id": "OIL-DMH-01",
            "name": "Damoh-01",
            "operator": "Oil India Limited",
            "field": "Damoh Block",
            "state": "Madhya Pradesh",
            "district": "Damoh",
            "latitude": 23.8420,
            "longitude": 79.4510,
            "total_depth": 3850.0,
            "spud_date": datetime.datetime(2019, 4, 10),
            "completion_date": datetime.datetime(2019, 9, 15),
            "well_type": "Exploratory / Deep Gas",
            "status": "Completed"
        },
        {
            "well_id": "OIL-DMH-04",
            "name": "Tendukheda-01",
            "operator": "Oil India Limited",
            "field": "Damoh Block",
            "state": "Madhya Pradesh",
            "district": "Damoh",
            "latitude": 23.7120,
            "longitude": 79.5230,
            "total_depth": 4100.0,
            "spud_date": datetime.datetime(2021, 2, 14),
            "completion_date": datetime.datetime(2021, 8, 20),
            "well_type": "Exploratory",
            "status": "Completed"
        },
        {
            "well_id": "ONGC-JBR-01",
            "name": "Jabera-01",
            "operator": "ONGC",
            "field": "Jabera Dome",
            "state": "Madhya Pradesh",
            "district": "Damoh",
            "latitude": 23.5410,
            "longitude": 79.7820,
            "total_depth": 4350.0,
            "spud_date": datetime.datetime(2018, 6, 1),
            "completion_date": datetime.datetime(2018, 12, 10),
            "well_type": "Deep Wildcat",
            "status": "Completed (Gas Discovery)"
        },
        {
            "well_id": "OIL-SHD-CBM-02",
            "name": "Shahdol-CBM-02",
            "operator": "Oil India Limited",
            "field": "Sohagpur CBM",
            "state": "Madhya Pradesh",
            "district": "Shahdol",
            "latitude": 23.3120,
            "longitude": 81.3650,
            "total_depth": 1450.0,
            "spud_date": datetime.datetime(2020, 1, 5),
            "completion_date": datetime.datetime(2020, 3, 18),
            "well_type": "CBM Core Hole",
            "status": "Completed"
        },
        {
            "well_id": "OIL-SHD-05",
            "name": "Sohagpur-Deep-05",
            "operator": "Oil India Limited",
            "field": "Sohagpur Basin",
            "state": "Madhya Pradesh",
            "district": "Shahdol",
            "latitude": 23.2450,
            "longitude": 81.4210,
            "total_depth": 2800.0,
            "spud_date": datetime.datetime(2021, 8, 12),
            "completion_date": datetime.datetime(2021, 11, 28),
            "well_type": "Appraisal",
            "status": "Completed"
        },
        {
            "well_id": "ONGC-KTN-01",
            "name": "Katni-Deep-01",
            "operator": "ONGC",
            "field": "Son Valley",
            "state": "Madhya Pradesh",
            "district": "Katni",
            "latitude": 23.8510,
            "longitude": 80.4120,
            "total_depth": 3600.0,
            "spud_date": datetime.datetime(2017, 3, 15),
            "completion_date": datetime.datetime(2017, 8, 5),
            "well_type": "Exploratory",
            "status": "Completed"
        },
        {
            "well_id": "ONGC-JBL-02",
            "name": "Jabalpur-South-02",
            "operator": "ONGC",
            "field": "Narmada Basin",
            "state": "Madhya Pradesh",
            "district": "Jabalpur",
            "latitude": 23.1520,
            "longitude": 79.9410,
            "total_depth": 3100.0,
            "spud_date": datetime.datetime(2019, 10, 10),
            "completion_date": datetime.datetime(2020, 2, 22),
            "well_type": "Stratigraphic Test",
            "status": "Completed"
        },

        # -------------------------------------------------------------
        # 2. ASSAM (Upper Assam Basin - Oil India Key Operational Field)
        # -------------------------------------------------------------
        {
            "well_id": "OIL-BGJ-01",
            "name": "Baghjan-01",
            "operator": "Oil India Limited",
            "field": "Baghjan",
            "state": "Assam",
            "district": "Tinsukia",
            "latitude": 27.5921,
            "longitude": 95.3942,
            "total_depth": 3950.0,
            "spud_date": datetime.datetime(2018, 3, 15),
            "completion_date": datetime.datetime(2018, 7, 20),
            "well_type": "Exploratory / Development",
            "status": "Completed"
        },
        {
            "well_id": "OIL-BGJ-05",
            "name": "Baghjan-05",
            "operator": "Oil India Limited",
            "field": "Baghjan",
            "state": "Assam",
            "district": "Tinsukia",
            "latitude": 27.6015,
            "longitude": 95.4051,
            "total_depth": 4120.0,
            "spud_date": datetime.datetime(2019, 6, 10),
            "completion_date": datetime.datetime(2019, 11, 2),
            "well_type": "Development",
            "status": "Completed"
        },
        {
            "well_id": "OIL-BGJ-09",
            "name": "Baghjan-09",
            "operator": "Oil India Limited",
            "field": "Baghjan",
            "state": "Assam",
            "district": "Tinsukia",
            "latitude": 27.5840,
            "longitude": 95.3850,
            "total_depth": 4250.0,
            "spud_date": datetime.datetime(2021, 1, 12),
            "completion_date": datetime.datetime(2021, 5, 29),
            "well_type": "Development",
            "status": "Completed"
        },
        {
            "well_id": "OIL-DGB-101",
            "name": "Digboi-101",
            "operator": "Oil India Limited",
            "field": "Digboi",
            "state": "Assam",
            "district": "Tinsukia",
            "latitude": 27.3820,
            "longitude": 95.6210,
            "total_depth": 2850.0,
            "spud_date": datetime.datetime(2015, 2, 10),
            "completion_date": datetime.datetime(2015, 5, 14),
            "well_type": "Appraisal",
            "status": "Completed"
        },
        {
            "well_id": "OIL-DGB-104",
            "name": "Digboi-104",
            "operator": "Oil India Limited",
            "field": "Digboi",
            "state": "Assam",
            "district": "Tinsukia",
            "latitude": 27.3910,
            "longitude": 95.6350,
            "total_depth": 3100.0,
            "spud_date": datetime.datetime(2017, 8, 5),
            "completion_date": datetime.datetime(2017, 12, 18),
            "well_type": "Development",
            "status": "Completed"
        },
        {
            "well_id": "OIL-NHK-42",
            "name": "Naharkatiya-42",
            "operator": "Oil India Limited",
            "field": "Naharkatiya",
            "state": "Assam",
            "district": "Dibrugarh",
            "latitude": 27.2855,
            "longitude": 95.3421,
            "total_depth": 3450.0,
            "spud_date": datetime.datetime(2016, 4, 1),
            "completion_date": datetime.datetime(2016, 7, 28),
            "well_type": "Development",
            "status": "Completed"
        },
        {
            "well_id": "OIL-NHK-58",
            "name": "Naharkatiya-58",
            "operator": "Oil India Limited",
            "field": "Naharkatiya",
            "state": "Assam",
            "district": "Dibrugarh",
            "latitude": 27.2990,
            "longitude": 95.3610,
            "total_depth": 3600.0,
            "spud_date": datetime.datetime(2019, 9, 14),
            "completion_date": datetime.datetime(2020, 1, 10),
            "well_type": "Development",
            "status": "Completed"
        },
        {
            "well_id": "OIL-MRN-24",
            "name": "Moran-24",
            "operator": "Oil India Limited",
            "field": "Moran",
            "state": "Assam",
            "district": "Dibrugarh",
            "latitude": 27.1840,
            "longitude": 94.9210,
            "total_depth": 3800.0,
            "spud_date": datetime.datetime(2018, 11, 20),
            "completion_date": datetime.datetime(2019, 3, 30),
            "well_type": "Exploratory",
            "status": "Completed"
        },
        {
            "well_id": "OIL-MRN-31",
            "name": "Moran-31",
            "operator": "Oil India Limited",
            "field": "Moran",
            "state": "Assam",
            "district": "Dibrugarh",
            "latitude": 27.1950,
            "longitude": 94.9450,
            "total_depth": 3950.0,
            "spud_date": datetime.datetime(2020, 5, 10),
            "completion_date": datetime.datetime(2020, 9, 22),
            "well_type": "Development",
            "status": "Completed"
        },
        {
            "well_id": "OIL-RDS-12",
            "name": "Rudrasagar-12",
            "operator": "Oil India Limited",
            "field": "Rudrasagar",
            "state": "Assam",
            "district": "Sivasagar",
            "latitude": 26.9740,
            "longitude": 94.6310,
            "total_depth": 3550.0,
            "spud_date": datetime.datetime(2018, 5, 10),
            "completion_date": datetime.datetime(2018, 9, 18),
            "well_type": "Development",
            "status": "Completed"
        },
        {
            "well_id": "OIL-GLK-45",
            "name": "Geleki-45",
            "operator": "Oil India Limited",
            "field": "Geleki",
            "state": "Assam",
            "district": "Sivasagar",
            "latitude": 26.8520,
            "longitude": 94.7210,
            "total_depth": 4200.0,
            "spud_date": datetime.datetime(2019, 7, 1),
            "completion_date": datetime.datetime(2019, 12, 14),
            "well_type": "Deep Producer",
            "status": "Completed"
        },

        # -------------------------------------------------------------
        # 3. GUJARAT (Cambay Basin)
        # -------------------------------------------------------------
        {
            "well_id": "OIL-GND-22",
            "name": "Gandhar-22",
            "operator": "Oil India Limited",
            "field": "Gandhar",
            "state": "Gujarat",
            "district": "Bharuch",
            "latitude": 21.8410,
            "longitude": 72.8210,
            "total_depth": 3400.0,
            "spud_date": datetime.datetime(2017, 4, 12),
            "completion_date": datetime.datetime(2017, 8, 20),
            "well_type": "Development",
            "status": "Completed"
        },
        {
            "well_id": "ONGC-ANK-14",
            "name": "Ankleshwar-14",
            "operator": "ONGC",
            "field": "Ankleshwar",
            "state": "Gujarat",
            "district": "Bharuch",
            "latitude": 21.6250,
            "longitude": 73.0120,
            "total_depth": 2750.0,
            "spud_date": datetime.datetime(2016, 9, 10),
            "completion_date": datetime.datetime(2016, 12, 18),
            "well_type": "Appraisal",
            "status": "Completed"
        },
        {
            "well_id": "ONGC-KLL-31",
            "name": "Kalol-31",
            "operator": "ONGC",
            "field": "Kalol",
            "state": "Gujarat",
            "district": "Gandhinagar",
            "latitude": 23.2410,
            "longitude": 72.4920,
            "total_depth": 2900.0,
            "spud_date": datetime.datetime(2019, 1, 15),
            "completion_date": datetime.datetime(2019, 5, 2),
            "well_type": "Development",
            "status": "Completed"
        },

        # -------------------------------------------------------------
        # 4. RAJASTHAN (Barmer-Sanchore & Jaisalmer Basins)
        # -------------------------------------------------------------
        {
            "well_id": "OIL-BMR-12",
            "name": "Mangala-Deep-12",
            "operator": "Oil India Limited / JV",
            "field": "Barmer Block",
            "state": "Rajasthan",
            "district": "Barmer",
            "latitude": 25.8210,
            "longitude": 71.4210,
            "total_depth": 2400.0,
            "spud_date": datetime.datetime(2018, 2, 10),
            "completion_date": datetime.datetime(2018, 5, 12),
            "well_type": "Development",
            "status": "Completed"
        },
        {
            "well_id": "OIL-JSL-04",
            "name": "Jaisalmer-Gas-04",
            "operator": "Oil India Limited",
            "field": "Dandewala Gas Field",
            "state": "Rajasthan",
            "district": "Jaisalmer",
            "latitude": 27.0210,
            "longitude": 70.8410,
            "total_depth": 2950.0,
            "spud_date": datetime.datetime(2019, 4, 1),
            "completion_date": datetime.datetime(2019, 7, 28),
            "well_type": "Exploratory Gas",
            "status": "Completed"
        },

        # -------------------------------------------------------------
        # 5. ANDHRA PRADESH (Krishna-Godavari Basin)
        # -------------------------------------------------------------
        {
            "well_id": "ONGC-PSR-19",
            "name": "Pasarlapudi-19",
            "operator": "ONGC",
            "field": "KG Onshore",
            "state": "Andhra Pradesh",
            "district": "East Godavari",
            "latitude": 16.5120,
            "longitude": 81.9410,
            "total_depth": 3750.0,
            "spud_date": datetime.datetime(2018, 8, 14),
            "completion_date": datetime.datetime(2019, 1, 10),
            "well_type": "High Pressure Gas",
            "status": "Completed"
        },

        # -------------------------------------------------------------
        # 6. WEST BENGAL (Bengal Basin)
        # -------------------------------------------------------------
        {
            "well_id": "ONGC-ASK-01",
            "name": "Ashoknagar-01",
            "operator": "ONGC",
            "field": "Bengal Onshore",
            "state": "West Bengal",
            "district": "North 24 Parganas",
            "latitude": 22.8310,
            "longitude": 88.6210,
            "total_depth": 3200.0,
            "spud_date": datetime.datetime(2020, 11, 1),
            "completion_date": datetime.datetime(2021, 3, 20),
            "well_type": "Discovery Producer",
            "status": "Completed"
        },

        # -------------------------------------------------------------
        # 7. TRIPURA (Tripura Fold Belt)
        # -------------------------------------------------------------
        {
            "well_id": "ONGC-AGT-06",
            "name": "Agartala-Dome-06",
            "operator": "ONGC",
            "field": "Agartala Gas Field",
            "state": "Tripura",
            "district": "West Tripura",
            "latitude": 23.8520,
            "longitude": 91.3120,
            "total_depth": 3150.0,
            "spud_date": datetime.datetime(2017, 10, 5),
            "completion_date": datetime.datetime(2018, 2, 14),
            "well_type": "Gas Producer",
            "status": "Completed"
        }
    ]

    for w_info in wells_data:
        well = Well(**w_info)
        db.add(well)
    db.commit()

    # Geological Formations by Basin
    mp_vindhyan_formations = [
        ("Alluvium & Soil Cover", 0, 150, "Alluvial Clay & Gravel", 0.30, 350.0, "Surface unconsolidated soil and gravel."),
        ("Bhander Sandstone", 150, 1100, "Red to purplish quartzitic Sandstone", 0.14, 25.0, "Hard abrasive quartzitic sandstone causing low ROP and bit wear."),
        ("Sirbu Shale", 1100, 1950, "Olive green to maroon laminated Shale", 0.08, 1.5, "Laminated swelling shale prone to borehole sloughing and tight hole."),
        ("Maihar Sandstone", 1950, 2600, "Fine-grained glauconitic Sandstone", 0.12, 15.0, "Tight gas bearing sandstone intervals with microfractures."),
        ("Rohtas Limestone", 2600, 3450, "Dense siliceous nodular Limestone", 0.06, 0.5, "Vuggy limestone prone to total mud losses / seepage loss."),
        ("Kaimur Sandstone (Basement)", 3450, 4400, "Massive silicified Quartzite", 0.05, 0.1, "Hard silicified basement sequence with high compressive strength.")
    ]

    assam_formations = [
        ("Alluvium & Dihing", 0, 450, "Unconsolidated Sand/Gravel", 0.32, 450.0, "Surface unconsolidated gravel beds and sands with washouts risk."),
        ("Tipam Sandstone (Upper)", 450, 1400, "Coarse to medium Sandstone", 0.26, 320.0, "Thick sandstone packages with highly porous channels. Prone to minor seepage losses."),
        ("Tipam Sandstone (Lower)", 1400, 2200, "Massive Sandstone with clay intercalations", 0.22, 180.0, "Massive permeable sandstone reservoir interval with depleted pressure in mature sections."),
        ("Girujan Clay / Surma", 2200, 2750, "Mottled Claystone & Siltstone", 0.15, 15.0, "Plastic swelling clays prone to bit balling and tight hole conditions."),
        ("Barail Coal-Shale", 2750, 3350, "Interbedded Coal, Carbonaceous Shale & Sand", 0.18, 45.0, "High pore pressure gas-bearing sands interbedded with splinty coals. Kick & packoff hotspot."),
        ("Kopili Formation", 3350, 3850, "Splintery Marine Shale with siltstone lenses", 0.10, 2.0, "Over-pressured brittle shale prone to sloughing, stuck pipe, and tight hole."),
        ("Sylhet / Jaintia Limestone", 3850, 4400, "Fossiliferous Nummulitic Limestone", 0.14, 60.0, "Naturally fractured vuggy limestone prone to total mud losses / cavernous zones.")
    ]

    gujarat_formations = [
        ("Post-Eocene Alluvium", 0, 600, "Sand and Clay", 0.28, 200.0, "Upper alluvium sequence."),
        ("Tarapur Shale", 600, 1600, "Grey to greenish fissile Shale", 0.12, 5.0, "Reactive swelling shale sequence."),
        ("Ankleshwar Sandstone", 1600, 2400, "Multi-layered deltaic Sandstone", 0.24, 180.0, "Major oil and gas producing sandstone package."),
        ("Cambay Shale", 2400, 3100, "Dark organic-rich fissile Shale", 0.08, 1.0, "Source rock shale prone to high overpressure kicks."),
        ("Deccan Trap (Basalt)", 3100, 3500, "Dense fractured Basalt", 0.04, 0.2, "Hard volcanic igneous floor.")
    ]

    # Insert Formations and Trajectories
    for w in db.query(Well).all():
        if w.state == "Madhya Pradesh":
            active_forms = mp_vindhyan_formations
            td_base = 4400.0
        elif w.state == "Gujarat":
            active_forms = gujarat_formations
            td_base = 3500.0
        else:
            active_forms = assam_formations
            td_base = 4400.0

        scale = w.total_depth / td_base

        for name, top, base, lith, poro, perm, desc in active_forms:
            adj_top = round(top * scale, 1)
            adj_base = round(min(base * scale, w.total_depth), 1)
            if adj_top < w.total_depth:
                f = Formation(
                    well_id=w.well_id,
                    formation_name=name,
                    top_depth_md=adj_top,
                    base_depth_md=adj_base,
                    lithology=lith,
                    porosity_avg=poro,
                    permeability_avg=perm,
                    description=desc
                )
                db.add(f)

        # Trajectory sample
        for md in range(0, int(w.total_depth) + 1, 100):
            inc = round(min(18.0, (md - 1000) * 0.012), 2) if md > 1000 else 0.0
            azi = round(40.0 + (md % 25), 2) if md > 1000 else 0.0
            tvd = round(md * 0.985 if md > 1000 else md, 1)
            traj = WellTrajectory(
                well_id=w.well_id,
                md=float(md),
                tvd=tvd,
                tvdss=tvd - 150.0,
                inclination=inc,
                azimuth=azi,
                dogleg_severity=0.4
            )
            db.add(traj)

    db.commit()

    # Historical Drilling Incidents and Verified Mitigations (Pan-India Grounded)
    incidents = [
        # MADHYA PRADESH INCIDENTS
        {
            "well_id": "OIL-DMH-01",
            "event_id": "EV-DMH01-01",
            "event_type": "Mud Loss",
            "start_depth_md": 2680.0,
            "end_depth_md": 2720.0,
            "formation_name": "Rohtas Limestone",
            "severity": "High",
            "npt_hours": 32.0,
            "description": "Total mud loss of 35 m3/hr encountered while drilling 8-1/2 inch section in cavernous / vuggy Rohtas Limestone with 1.22 SG mud.",
            "root_cause": "Encountered karstified sub-hydrostatic fracture network in Rohtas Limestone.",
            "source_document": "WCR_OIL_DMH01_FINAL.pdf",
            "page_number": 56,
            "evidence_text": "Sudden drop in flow out to 0% at 2694 m MD. Lost 28 m3 active pit mud in 20 minutes.",
            "extraction_confidence": 0.98,
            "mitigation": {
                "mitigation_id": "MIT-DMH01-01",
                "action_taken": "Pumed 30 m3 high-solid thixotropic cross-linked LCM pill (calcium carbonate blend 40 ppb + mica + fibrous sealant). Hesitation squeeze applied.",
                "outcome": "Circulation restored successfully. Casing shoe set at 2750 m to isolate loss zone.",
                "success_flag": True,
                "recommended_preventive_practice": "Pre-treat mud with 15 ppb sized bridging agents before entering Rohtas Limestone. Lower pump rate to 500 gpm to minimize ECD.",
                "source_reference": "OIL Central India Basin Drilling SOP-21"
            }
        },
        {
            "well_id": "OIL-DMH-01",
            "event_id": "EV-DMH01-02",
            "event_type": "Gas Kick",
            "start_depth_md": 3480.0,
            "end_depth_md": 3520.0,
            "formation_name": "Kaimur Sandstone (Basement)",
            "severity": "High",
            "npt_hours": 28.0,
            "description": "Deep tight gas kick observed with 3.8 m3 pit gain and 380 psi shut-in drillpipe pressure (SIDPP).",
            "root_cause": "Encountered deep overpressured natural gas fracture pocket in Vindhyan Kaimur horizon.",
            "source_document": "DDR_OIL_DMH01_20190818.pdf",
            "page_number": 32,
            "evidence_text": "Drilling break from 6 m/h to 24 m/h. Gas detector spiked to 65%. Well shut in on annular BOP.",
            "extraction_confidence": 0.97,
            "mitigation": {
                "mitigation_id": "MIT-DMH01-02",
                "action_taken": "Killed well using Wait and Weight method. Raised mud density from 1.18 SG to 1.30 SG.",
                "outcome": "Gas circulated out safely through mud-gas separator. Well stabilized.",
                "success_flag": True,
                "recommended_preventive_practice": "Maintain minimum 1.28 SG mud weight across Kaimur sand sequence and maintain degasser unit on high alert.",
                "source_reference": "Vindhyan Basin Deep Drilling Safety Review"
            }
        },
        {
            "well_id": "OIL-DMH-04",
            "event_id": "EV-DMH04-01",
            "event_type": "Stuck Pipe",
            "start_depth_md": 1420.0,
            "end_depth_md": 1460.0,
            "formation_name": "Sirbu Shale",
            "severity": "High",
            "npt_hours": 42.0,
            "description": "BHA stuck while making connection due to sloughing Sirbu shale packoff.",
            "root_cause": "Hydration and stress relief in laminated Sirbu shale leading to mechanical borehole collapse.",
            "source_document": "WCR_OIL_DMH04.pdf",
            "page_number": 44,
            "evidence_text": "Pump pressure skyrocketed to 280 bar with zero string rotation possible at 1445 m.",
            "extraction_confidence": 0.96,
            "mitigation": {
                "mitigation_id": "MIT-DMH04-01",
                "action_taken": "Jarred string down with 110 klbs jar impact. Pumped 18 m3 low-viscosity surfactant freeing pill and restored mud KCl concentration to 7%.",
                "outcome": "Pipe freed after 6 hours jarring. Tripped out cleanly.",
                "success_flag": True,
                "recommended_preventive_practice": "Use high-inhibition KCl-polyamine mud system with >=6% KCl to inhibit Sirbu shale swelling.",
                "source_reference": "OIL Well Engineering Directorate Bulletin MP-04"
            }
        },
        {
            "well_id": "OIL-SHD-CBM-02",
            "event_id": "EV-SHD02-01",
            "event_type": "Gas Kick",
            "start_depth_md": 920.0,
            "end_depth_md": 950.0,
            "formation_name": "Maihar Sandstone",
            "severity": "Moderate",
            "npt_hours": 18.0,
            "description": "Shallow coal-bed methane influx into wellbore while coring coal seam.",
            "root_cause": "Desorbing methane gas from fractured coal cleats at low hydrostatic overbalance.",
            "source_document": "DDR_OIL_SHDCBM_20200214.pdf",
            "page_number": 14,
            "evidence_text": "Methane gas detected at shale shaker; pit gain 1.8 m3.",
            "extraction_confidence": 0.94,
            "mitigation": {
                "mitigation_id": "MIT-SHD02-01",
                "action_taken": "Circulated bottoms-up through degasser. Weighted mud from 1.08 to 1.16 SG.",
                "outcome": "Gas influx extinguished, core recovery completed.",
                "success_flag": True,
                "recommended_preventive_practice": "Maintain continuous degassing and 1.15 SG mud weight when penetrating coal seams in Sohagpur CBM.",
                "source_reference": "CBM Drilling Best Practices Manual"
            }
        },

        # ASSAM INCIDENTS
        {
            "well_id": "OIL-BGJ-01",
            "event_id": "EV-BGJ01-01",
            "event_type": "Mud Loss",
            "start_depth_md": 1540.0,
            "end_depth_md": 1580.0,
            "formation_name": "Tipam Sandstone (Lower)",
            "severity": "Moderate",
            "npt_hours": 14.5,
            "description": "Partial mud loss of 18 m3/hr in porous Tipam sand channels with 1.18 SG water-based mud.",
            "root_cause": "Encountered depleted sub-hydrostatic permeable sandstone bed.",
            "source_document": "WCR_OIL_BGJ01_FINAL.pdf",
            "page_number": 42,
            "evidence_text": "Observed pit drop at 1548 m. Flow out decreased from 100% to 68%.",
            "extraction_confidence": 0.98,
            "mitigation": {
                "mitigation_id": "MIT-BGJ01-01",
                "action_taken": "Pumped 25 m3 LCM pill (medium walnut shells + CaCO3). Soaked for 2.5 hours.",
                "outcome": "Full circulation restored.",
                "success_flag": True,
                "recommended_preventive_practice": "Pre-treat active system with 10-15 ppb fine CaCO3 before drilling below 1500 m in Tipam.",
                "source_reference": "OIL Drilling Standard SOP-14/ASSAM"
            }
        },
        {
            "well_id": "OIL-BGJ-01",
            "event_id": "EV-BGJ01-02",
            "event_type": "Gas Kick",
            "start_depth_md": 2980.0,
            "end_depth_md": 3020.0,
            "formation_name": "Barail Coal-Shale",
            "severity": "High",
            "npt_hours": 36.0,
            "description": "Drilling break at 2992 m followed by flow check positive with 4.5 m3 pit gain and 420 psi SIDPP.",
            "root_cause": "Unexpected high pore-pressure gas pocket inside Barail Coal-Shale sequence.",
            "source_document": "DDR_OIL_BGJ01_20180512.pdf",
            "page_number": 18,
            "evidence_text": "ROP jumped from 12 m/h to 38 m/h at 2992m MD. Well shut in on annular BOP; SIDPP=420 psi.",
            "extraction_confidence": 0.99,
            "mitigation": {
                "mitigation_id": "MIT-BGJ01-02",
                "action_taken": "Executed Wait & Weight kill method. Circulated out gas influx and raised mud weight from 1.20 to 1.32 SG.",
                "outcome": "Well successfully killed with zero residual surface pressure.",
                "success_flag": True,
                "recommended_preventive_practice": "Slow pump rate checks every shift prior to entering Barail Coal-Shale (2800m+). Weighted mud on standby.",
                "source_reference": "Well Control Incident Review BGJ-2018"
            }
        },
        {
            "well_id": "OIL-BGJ-05",
            "event_id": "EV-BGJ05-01",
            "event_type": "Gas Kick",
            "start_depth_md": 3050.0,
            "end_depth_md": 3090.0,
            "formation_name": "Barail Coal-Shale",
            "severity": "High",
            "npt_hours": 28.0,
            "description": "Gas influx at 3065 m MD. Background gas spiked to 48%. Pit gain 3.2 m3.",
            "root_cause": "Overpressured lenticular sand stringer within Barail coal sequence.",
            "source_document": "WCR_OIL_BGJ05.pdf",
            "page_number": 65,
            "evidence_text": "Pit gain 3.2 m3 detected at 3065m. SIDPP=310 psi, SICP=450 psi.",
            "extraction_confidence": 0.97,
            "mitigation": {
                "mitigation_id": "MIT-BGJ05-01",
                "action_taken": "Shut in well, circulated out influx using Driller's Method. Increased mud weight to 1.31 SG.",
                "outcome": "Gas removed cleanly, well static on flow check.",
                "success_flag": True,
                "recommended_preventive_practice": "Maintain mud density minimum 1.29–1.31 SG across 2950–3200 m interval to avoid underbalanced kicks.",
                "source_reference": "OIL Well Engineering Directorate Report Vol 8"
            }
        },
        {
            "well_id": "OIL-BGJ-05",
            "event_id": "EV-BGJ05-02",
            "event_type": "Stuck Pipe",
            "start_depth_md": 3480.0,
            "end_depth_md": 3520.0,
            "formation_name": "Kopili Formation",
            "severity": "High",
            "npt_hours": 44.0,
            "description": "Differential sticking occurred during connection in Kopili shale with high overbalance.",
            "root_cause": "Excessive filter cake thickness and high hydrostatic overbalance (mud weight 1.34 SG).",
            "source_document": "DDR_OIL_BGJ05_OCT2019.pdf",
            "page_number": 88,
            "evidence_text": "String immobile after 18 min stationary connection at 3495 m MD. Overpull exceeded 80 klbs.",
            "extraction_confidence": 0.96,
            "mitigation": {
                "mitigation_id": "MIT-BGJ05-02",
                "action_taken": "Spotted 18 m3 pipe-freeing lubricant pill. Applied hydraulic jar upward at 95 klbs for 4 hours.",
                "outcome": "String freed after 4.2 hours soaking and jarring.",
                "success_flag": True,
                "recommended_preventive_practice": "Strictly limit stationary string time to <5 mins in Kopili. Keep fluid loss <= 3.5 ml.",
                "source_reference": "OIL Drilling Troubles Guide Ch-4"
            }
        },

        # GUJARAT INCIDENT
        {
            "well_id": "OIL-GND-22",
            "event_id": "EV-GND22-01",
            "event_type": "Stuck Pipe",
            "start_depth_md": 2480.0,
            "end_depth_md": 2520.0,
            "formation_name": "Cambay Shale",
            "severity": "High",
            "npt_hours": 38.0,
            "description": "Mechanical sticking due to swelling and sloughing of high-plasticity Cambay Shale.",
            "root_cause": "Inadequate shale inhibition causing reactive clay swelling and tight hole.",
            "source_document": "WCR_OIL_GND22.pdf",
            "page_number": 38,
            "evidence_text": "Torque exceeded 28 kNm at 2495 m MD. Unable to rotate or reciprocate string.",
            "extraction_confidence": 0.95,
            "mitigation": {
                "mitigation_id": "MIT-GND22-01",
                "action_taken": "Circulated glycol-based inhibitor sweep, jarred down with 85 klbs. Raised mud weight from 1.18 to 1.25 SG.",
                "outcome": "String freed, hole reamed with roller reamers.",
                "success_flag": True,
                "recommended_preventive_practice": "Maintain glycol/polyamine inhibition above 5% when drilling through Cambay Shale.",
                "source_reference": "Cambay Basin Drilling Operations Standard"
            }
        },

        # RAJASTHAN INCIDENT
        {
            "well_id": "OIL-JSL-04",
            "event_id": "EV-JSL04-01",
            "event_type": "Mud Loss",
            "start_depth_md": 1820.0,
            "end_depth_md": 1860.0,
            "formation_name": "Jaisalmer Limestone",
            "severity": "High",
            "npt_hours": 24.0,
            "description": "Seepage to partial losses in fractured Jaisalmer limestone with high permeability.",
            "root_cause": "Sub-hydrostatic naturally fractured carbonate interval.",
            "source_document": "DDR_OIL_JSL04_2019.pdf",
            "page_number": 21,
            "evidence_text": "Lost 14 m3/hr at 1835 m MD. Standpipe pressure dropped 20 bar.",
            "extraction_confidence": 0.94,
            "mitigation": {
                "mitigation_id": "MIT-JSL04-01",
                "action_taken": "Pumped engineered fiber LCM pill (20 ppb calcium carbonate + 8 ppb mica).",
                "outcome": "Loss rate dropped to 0 m3/hr.",
                "success_flag": True,
                "recommended_preventive_practice": "Keep LCM materials pre-mixed in slug pit before penetrating Jaisalmer limestone.",
                "source_reference": "Western Desert Drilling Operations SOP"
            }
        }
    ]

    for ev_data in incidents:
        mit_data = ev_data.pop("mitigation")
        event = DrillingEvent(**ev_data)
        db.add(event)
        db.commit()

        mit = Mitigation(
            mitigation_id=mit_data["mitigation_id"],
            event_id=event.event_id,
            well_id=event.well_id,
            action_taken=mit_data["action_taken"],
            outcome=mit_data["outcome"],
            success_flag=mit_data["success_flag"],
            recommended_preventive_practice=mit_data["recommended_preventive_practice"],
            source_reference=mit_data["source_reference"]
        )
        db.add(mit)

    db.commit()

    # Telemetry streaming data (500 records for live replay)
    start_time = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    current_depth = 2950.0
    telemetries = []
    
    for i in range(500):
        t_time = start_time + datetime.timedelta(minutes=i * 2)
        current_depth += random.uniform(0.1, 0.35)
        
        is_anomaly = False
        anomaly_type = None

        wob = random.gauss(110.0, 7.0)
        rpm = random.gauss(120.0, 5.0)
        torque = random.gauss(14.0, 1.2)
        rop = random.gauss(15.0, 2.0)
        spp = random.gauss(185.0, 5.0)
        flow_in = random.gauss(650.0, 10.0)
        mud_weight = 1.20
        hookload = random.gauss(1350.0, 20.0)

        # Gas kick signature at 2991-2996m
        if 2991.0 <= current_depth <= 2996.0:
            is_anomaly = True
            anomaly_type = "Gas Kick / Influx Indicator"
            rop += 24.0 # Drilling break
            spp -= 20.0 # Pressure drop
            torque += 6.0
            flow_in += 50.0

        telemetry = DrillingTelemetry(
            well_id="OIL-BGJ-01",
            timestamp=t_time,
            depth_md=round(current_depth, 2),
            wob=round(wob, 2),
            rpm=round(rpm, 1),
            torque=round(torque, 2),
            rop=round(rop, 2),
            spp=round(spp, 1),
            flow_in=round(flow_in, 1),
            mud_weight=round(mud_weight, 2),
            hookload=round(hookload, 1),
            is_anomaly=is_anomaly,
            anomaly_type=anomaly_type
        )
        telemetries.append(telemetry)

    db.bulk_save_objects(telemetries)
    db.commit()

    print(f"[SUCCESS] Pan-India NWIS Database seeded with {len(wells_data)} wells, {len(incidents)} incidents, and {len(telemetries)} telemetry records.")
    if close_db:
        db.close()

if __name__ == "__main__":
    seed_database(force=True)
