import sys

sys.path.insert(0, "apps/api")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import ChainOfCustodyEvent, Evidence, ForensicCase
from app.services.case_service import CaseService
from app.services.evidence_import_service import EvidenceImportService


def create_test_database():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)

    return Session()


def test_evidence_import():
    db = create_test_database()

    case = CaseService.create_case(
        db=db,
        case_number="SIH-26150-001",
        title="Demo DVR Investigation",
        description="Synthetic DVR forensic investigation.",
    )

    service = EvidenceImportService()

    evidence = service.import_evidence(
        db=db,
        case_id=case.id,
        evidence_path="fixtures/demo_dvr/demo_dvr.img",
    )

    assert evidence.id.startswith("EVIDENCE-")
    assert evidence.filename == "demo_dvr.img"
    assert evidence.size_bytes > 0
    assert len(evidence.sha256) == 64
    assert evidence.vendor == "DemoSecure"
    assert evidence.status == "DETECTED"

    events = (
        db.query(ChainOfCustodyEvent)
        .filter(
            ChainOfCustodyEvent.evidence_id == evidence.id
        )
        .order_by(ChainOfCustodyEvent.id.asc())
        .all()
    )

    assert len(events) == 3
    assert events[0].action == "IMPORTED"
    assert events[1].action == "HASHED"
    assert events[2].action == "DETECTED"

    db.close()
