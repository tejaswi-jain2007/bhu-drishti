import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

class LASLogParser:
    @staticmethod
    def parse_las_file(file_path: str) -> Dict[str, Any]:
        """
        Parse standard .las well log file and extract curve metadata and statistics.
        """
        try:
            import lasio
            las = lasio.read(file_path)
            df = las.df()
            
            curves = list(las.curves.keys())
            header = {item.mnemonic: item.value for item in las.well}
            
            return {
                "well_name": header.get("WELL", Path(file_path).stem),
                "start_depth": las.well.STRT.value if hasattr(las.well, "STRT") else df.index.min(),
                "stop_depth": las.well.STOP.value if hasattr(las.well, "STOP") else df.index.max(),
                "step": las.well.STEP.value if hasattr(las.well, "STEP") else None,
                "curves": curves,
                "total_rows": len(df),
                "summary_stats": {
                    col: {
                        "min": round(float(df[col].min()), 2) if not pd.isna(df[col].min()) else None,
                        "max": round(float(df[col].max()), 2) if not pd.isna(df[col].max()) else None,
                        "mean": round(float(df[col].mean()), 2) if not pd.isna(df[col].mean()) else None
                    }
                    for col in df.columns[:8]
                }
            }
        except Exception as e:
            return {
                "file_path": file_path,
                "status": "error",
                "message": f"Failed to parse LAS: {str(e)}"
            }
