from __future__ import annotations

from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.case import ForensicCase


class CaseService:

    @staticmethod
    def create_case(
        db: Session,
        case_number: str,
        title: str,
        description: str | None = None,
    ) -> ForensicCase:

        case = ForensicCase(
            id=f"CASE-{uuid4().hex[:12].upper()}",
            case_number=case_number,
            title=title,
            description=description,
            status="OPEN",
        )

        db.add(case)
        db.commit()
        db.refresh(case)

        return case
