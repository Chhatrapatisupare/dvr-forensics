from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.evidence import Evidence
from app.services.custody_service import ChainOfCustodyService


router = APIRouter(
    prefix="/api/evidence",
    tags=["Verification"],
)


@router.post("/{evidence_id}/verify")
def verify_evidence(
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
            detail="Evidence not found.",
        )

    chain_valid = ChainOfCustodyService().verify_chain(
        db=db,
        case_id=evidence.case_id,
        evidence_id=evidence.id,
    )

    return {
        "evidence_id": evidence.id,
        "sha256": evidence.sha256,
        "chain_valid": chain_valid,
        "integrity_status": (
            "VERIFIED"
            if chain_valid
            else "TAMPERED"
        ),
    }
