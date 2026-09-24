from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.case import ForensicCase
from app.schemas.case import CaseCreate, CaseResponse
from app.services.case_service import CaseService


router = APIRouter(
    prefix="/api/cases",
    tags=["Cases"],
)


@router.post(
    "",
    response_model=CaseResponse,
)
def create_case(
    payload: CaseCreate,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(ForensicCase)
        .filter(
            ForensicCase.case_number
            == payload.case_number
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Case number already exists.",
        )

    return CaseService.create_case(
        db=db,
        case_number=payload.case_number,
        title=payload.title,
        description=payload.description,
    )


@router.get(
    "/{case_id}",
    response_model=CaseResponse,
)
def get_case(
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
            detail="Case not found.",
        )

    return case
