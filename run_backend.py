import uvicorn
import os

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_dir)
    print("Starting NWIS FastAPI Backend on http://127.0.0.1:8000 ...")
    print("Interactive Swagger Documentation: http://127.0.0.1:8000/docs")
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
