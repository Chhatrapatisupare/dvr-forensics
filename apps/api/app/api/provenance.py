from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.evidence import Evidence
from app.schemas.provenance import ProvenanceResponse
from app.services.provenance_service import ProvenanceService


router = APIRouter(
    prefix="/api",
    tags=["Provenance"],
)


@router.get(
    "/evidence/{evidence_id}/provenance",
    response_model=ProvenanceResponse,
)
def get_provenance(
    evidence_id: str,
    db: Session = Depends(get_db),
):
    evidence = (
        db.query(Evidence)
        .filter(Evidence.id == evidence_id)
        .first()
    )

    if evidence is None:
        raise HTTPException(
            status_code=404,
            detail="Evidence not found.",
        )

    try:
        return ProvenanceService().build_graph(
            db=db,
            evidence_id=evidence_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )