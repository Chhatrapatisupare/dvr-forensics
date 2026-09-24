from pathlib import Path
import sys

APP_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = APP_ROOT.parents[2]

for path in (APP_ROOT, PROJECT_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.cases import router as cases_router
from app.api.evidence import router as evidence_router
from app.api.recordings import router as recordings_router
from app.api.verification import router as verification_router
from app.api.timeline import router as timeline_router
from app.api.recovery import router as recovery_router
from app.api.provenance import router as provenance_router

from app.services.database_service import initialize_database


initialize_database()


app = FastAPI(
    title="DVR/NVR Forensic Analysis Tool",
    description=(
        "SIH26150 - Multi-Vendor DVR/NVR "
        "Forensic Analysis Platform"
    ),
    version="0.3.0",
)


# Frontend CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(cases_router)
app.include_router(evidence_router)
app.include_router(recordings_router)
app.include_router(verification_router)
app.include_router(timeline_router)
app.include_router(recovery_router)
app.include_router(provenance_router)


@app.get("/")
def root():
    return {
        "name": "DVR/NVR Forensic Analysis Tool",
        "project": "SIH26150",
        "status": "running",
        "version": "0.3.0",
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "forensic-api",
    }