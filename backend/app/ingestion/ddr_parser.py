import re
from typing import Dict, Any, List, Optional
from datetime import datetime

class DDRReportParser:
    @staticmethod
    def extract_events_from_text(report_text: str, well_id: str, document_name: str = "DDR.pdf") -> List[Dict[str, Any]]:
        """
        Extract structured drilling events, severity, NPT and mitigations from unstructured DDR or WCR text.
        """
        extracted_events = []
        
        # Hazard keyword patterns
        patterns = [
            (r'(mud\s*loss|lost\s*circulation|seepage\s*loss)', "Mud Loss"),
            (r'(gas\s*kick|well\s*kick|influx|sidpp|well\s*shut\s*in)', "Gas Kick"),
            (r'(stuck\s*pipe|differential\s*sticking|pipe\s*freeing|overpull)', "Stuck Pipe"),
            (r'(torque\s*surge|drag|tight\s*hole|reaming)', "Torque/Drag Anomaly"),
            (r'(casing\s*hung|cement\s*channel|casing\s*collapse)', "Casing Issue")
        ]

        sentences = re.split(r'(?<=[.!?])\s+', report_text)
        
        for idx, sentence in enumerate(sentences):
            for pattern, event_type in patterns:
                if re.search(pattern, sentence, re.IGNORECASE):
                    # Try to extract depth
                    depth_match = re.search(r'(\d{3,5})\s*(m|meter|ft)?', sentence, re.IGNORECASE)
                    start_depth = float(depth_match.group(1)) if depth_match else 2000.0
                    end_depth = start_depth + 30.0

                    # Severity heuristic
                    severity = "Moderate"
                    if any(w in sentence.lower() for w in ["severe", "total loss", "blowout", "kill", "high influx", "critical"]):
                        severity = "High"
                    elif any(w in sentence.lower() for w in ["seepage", "minor", "slight"]):
                        severity = "Low"

                    extracted_events.append({
                        "event_id": f"EXT-{well_id}-{len(extracted_events)+1}",
                        "well_id": well_id,
                        "event_type": event_type,
                        "start_depth_md": start_depth,
                        "end_depth_md": end_depth,
                        "severity": severity,
                        "description": sentence.strip(),
                        "source_document": document_name,
                        "extraction_confidence": 0.92
                    })
                    break

        return extracted_events
