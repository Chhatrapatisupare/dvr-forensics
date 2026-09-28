from fastapi import APIRouter, HTTPException, Query

from app.services.analytics import run_analytics
from app.services.dataset_generator import generate_dataset

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/runs")
def get_analytics_run(
    profile: str = Query(default="MIXED"),
    size: int = Query(default=20, ge=1, le=200),
):
    try:
        records = generate_dataset(profile=profile, seed=42, size=size)
        result = run_analytics(records)
        result["profile"] = profile
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
