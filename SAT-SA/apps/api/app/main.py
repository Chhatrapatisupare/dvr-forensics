from fastapi import FastAPI

from app.routers.analytics import router as analytics_router

app = FastAPI(title="SAT-SA API", version="0.1.0")

app.include_router(analytics_router, prefix="/api")


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "service": "sat-sa-api"}
