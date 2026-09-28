from fastapi.testclient import TestClient

from app.main import app
from app.services.analytics import run_analytics
from app.services.dataset_generator import generate_dataset
from app.services.validation import validate_records


client = TestClient(app)


def test_dataset_generation_for_normal_profile():
    records = generate_dataset(profile="NORMAL", seed=42, size=25)

    assert len(records) == 25
    assert all("entity_id" in r for r in records)
    assert all("status" in r for r in records)
    assert all(r["profile"] == "NORMAL" for r in records)


def test_validation_rejects_invalid_data():
    bad = [{
        "entity_id": "E-001",
        "case_id": "C-001",
        "timestamp": "2025-03-01T00:00:00",
        "status": "INVALID_STATUS",
        "investigation_days": 2,
        "escalation_days": 1,
        "closure_days": 3,
        "backlog_count": 1,
        "peer_group": "GROUP_A",
        "profile": "NORMAL",
    }]

    result = validate_records(bad)
    assert result["valid"] is False
    assert len(result["errors"]) >= 1


def test_analytics_produces_findings_for_generated_dataset():
    records = generate_dataset(profile="MIXED", seed=42, size=40)
    result = run_analytics(records)

    assert result["total_records"] == 40
    assert "findings" in result
    assert isinstance(result["findings"], list)
    assert "summary" in result


def test_health_and_analytics_endpoints():
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    run = client.get("/api/analytics/runs?profile=MIXED&size=20")
    assert run.status_code == 200
    payload = run.json()
    assert payload["profile"] == "MIXED"
    assert payload["total_records"] == 20
    assert "findings" in payload
