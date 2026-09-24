import sys

sys.path.insert(0, "apps/api")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import ChainOfCustodyEvent
from app.services.custody_service import ChainOfCustodyService


def create_test_database():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)

    return Session()


def test_chain_creation():
    db = create_test_database()

    service = ChainOfCustodyService()

    first = service.add_event(
        db=db,
        case_id="CASE-001",
        evidence_id="EVIDENCE-001",
        action="IMPORTED",
        description="Evidence image imported.",
    )

    second = service.add_event(
        db=db,
        case_id="CASE-001",
        evidence_id="EVIDENCE-001",
        action="HASHED",
        description="SHA-256 calculated.",
    )

    assert first.previous_hash is None
    assert first.event_hash

    assert second.previous_hash == first.event_hash
    assert second.event_hash

    assert first.event_hash != second.event_hash

    db.close()


def test_chain_verification():
    db = create_test_database()

    service = ChainOfCustodyService()

    service.add_event(
        db=db,
        case_id="CASE-002",
        evidence_id="EVIDENCE-002",
        action="IMPORTED",
        description="Evidence imported.",
    )

    service.add_event(
        db=db,
        case_id="CASE-002",
        evidence_id="EVIDENCE-002",
        action="HASHED",
        description="Evidence hashed.",
    )

    service.add_event(
        db=db,
        case_id="CASE-002",
        evidence_id="EVIDENCE-002",
        action="VERIFIED",
        description="Evidence integrity verified.",
    )

    assert service.verify_chain(
        db,
        "CASE-002",
        "EVIDENCE-002",
    ) is True

    db.close()


def test_tamper_detection():
    db = create_test_database()

    service = ChainOfCustodyService()

    service.add_event(
        db=db,
        case_id="CASE-003",
        evidence_id="EVIDENCE-003",
        action="IMPORTED",
        description="Evidence imported.",
    )

    event = service.add_event(
        db=db,
        case_id="CASE-003",
        evidence_id="EVIDENCE-003",
        action="HASHED",
        description="Evidence hashed.",
    )

    event.description = "Tampered description"
    db.commit()

    assert service.verify_chain(
        db,
        "CASE-003",
        "EVIDENCE-003",
    ) is False

    db.close()
