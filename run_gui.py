import subprocess
import sys
import os

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    print("Launching NWIS Interactive Python GUI Dashboard...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "gui/app_gui.py"])
