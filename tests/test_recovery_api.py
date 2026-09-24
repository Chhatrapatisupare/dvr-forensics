import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
API_PATH = PROJECT_ROOT / "apps" / "api"

sys.path.insert(0, str(API_PATH))

from fastapi.testclient import TestClient

from app.main import app
from app.database import SessionLocal
from app.models.recovery import RecoveryArtifactRecord
from app.models.custody import ChainOfCustodyEvent


client = TestClient(app)

EVIDENCE_ID = "EVIDENCE-C92B2AADB8F1"


def test_recovery_api_returns_existing_artifact():
    response = client.post(
        f"/api/evidence/{EVIDENCE_ID}/recover",
        json={
            "recording_id": "REC-003",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["evidence_id"] == EVIDENCE_ID
    assert data["recording_id"] == "REC-003"
    assert data["status"] == "RECOVERED"
    assert data["confidence"] == "DEMO"
    assert data["method"] == "DemoSecure synthetic recovery"


def test_recovery_api_is_idempotent():
    first_response = client.post(
        f"/api/evidence/{EVIDENCE_ID}/recover",
        json={
            "recording_id": "REC-003",
        },
    )

    second_response = client.post(
        f"/api/evidence/{EVIDENCE_ID}/recover",
        json={
            "recording_id": "REC-003",
        },
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    first = first_response.json()
    second = second_response.json()

    assert first["id"] == second["id"]
    assert first["sha256"] == second["sha256"]


def test_recovery_api_does_not_create_duplicate_database_records():
    db = SessionLocal()

    try:
        artifacts = (
            db.query(RecoveryArtifactRecord)
            .filter(
                RecoveryArtifactRecord.evidence_id == EVIDENCE_ID,
                RecoveryArtifactRecord.recording_id == "REC-003",
            )
            .all()
        )

        assert len(artifacts) == 1

    finally:
        db.close()


def test_recovery_api_does_not_create_duplicate_custody_events():
    db = SessionLocal()

    try:
        events = (
            db.query(ChainOfCustodyEvent)
            .filter(
                ChainOfCustodyEvent.evidence_id == EVIDENCE_ID,
                ChainOfCustodyEvent.action == "RECOVERED",
            )
            .all()
        )

        assert len(events) == 1

    finally:
        db.close()