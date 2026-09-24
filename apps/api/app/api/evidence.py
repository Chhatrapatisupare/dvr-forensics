from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.case import ForensicCase
from app.models.evidence import Evidence
from app.schemas.evidence import (
    EvidenceImportRequest,
    EvidenceResponse,
)
from app.services.custody_service import ChainOfCustodyService
from app.services.evidence_import_service import EvidenceImportService


router = APIRouter(prefix="/api", tags=["Evidence"])


@router.post(
    "/cases/{case_id}/evidence",
    response_model=EvidenceResponse,
)
def import_evidence(
    case_id: str,
    request: EvidenceImportRequest,
    db: Session = Depends(get_db),
):
    case = (
        db.query(ForensicCase)
        .filter(ForensicCase.id == case_id)
        .first()
    )

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found",
        )

    try:
        service = EvidenceImportService()

        return service.import_evidence(
            db=db,
            case_id=case_id,
            evidence_path=request.evidence_path,
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.get(
    "/cases/{case_id}/evidence",
    response_model=list[EvidenceResponse],
)
def list_evidence(
    case_id: str,
    db: Session = Depends(get_db),
):
    case = (
        db.query(ForensicCase)
        .filter(ForensicCase.id == case_id)
        .first()
    )

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found",
        )

    return (
        db.query(Evidence)
        .filter(Evidence.case_id == case_id)
        .order_by(Evidence.imported_at.asc())
        .all()
    )


@router.get(
    "/evidence/{evidence_id}/custody",
)
def get_custody(
    evidence_id: str,
    db: Session = Depends(get_db),
):
    evidence = (
        db.query(Evidence)
        .filter(Evidence.id == evidence_id)
        .first()
    )

    if not evidence:
        raise HTTPException(
            status_code=404,
            detail="Evidence not found",
        )

    service = ChainOfCustodyService()

    return service.get_events(
        db=db,
        case_id=evidence.case_id,
        evidence_id=evidence_id,
    )


@router.get(
    "/evidence",
    response_model=list[EvidenceResponse],
)
def list_all_evidence(
    db: Session = Depends(get_db),
):
    return (
        db.query(Evidence)
        .order_by(Evidence.imported_at.asc())
        .all()
    )