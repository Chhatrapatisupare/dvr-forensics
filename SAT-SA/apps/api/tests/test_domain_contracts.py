from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from app.schemas.domain import Case, Entity, FindingEvidence, SupervisoryScore


def test_valid_entity_and_case_contracts():
    entity = Entity(
        entity_id="ENTITY-0001",
        entity_name="SOC Alpha",
        entity_type="SOC",
        sector="Government",
        peer_group="TIER_1",
        active=True,
    )
    assert entity.entity_id == "ENTITY-0001"

    case = Case(
        case_id="CASE-000001",
        entity_id="ENTITY-0001",
        alert_id="ALERT-000001",
        created_at=datetime(2026, 1, 15, 9, 35, tzinfo=timezone.utc),
        assigned_at=datetime(2026, 1, 15, 9, 40, tzinfo=timezone.utc),
        investigation_started=datetime(2026, 1, 15, 9, 50, tzinfo=timezone.utc),
        investigation_completed=datetime(2026, 1, 15, 11, 10, tzinfo=timezone.utc),
        escalated_at=None,
        closed_at=datetime(2026, 1, 15, 12, 0, tzinfo=timezone.utc),
        resolution="Benign activity",
        closure_reason="Verified by analyst",
    )
    assert case.case_id == "CASE-000001"


def test_invalid_case_timeline_is_rejected():
    with pytest.raises(ValidationError):
        Case(
            case_id="CASE-000002",
            entity_id="ENTITY-0001",
            alert_id="ALERT-000002",
            created_at=datetime(2026, 1, 15, 11, 0, tzinfo=timezone.utc),
            assigned_at=datetime(2026, 1, 15, 9, 40, tzinfo=timezone.utc),
            investigation_started=None,
            investigation_completed=None,
            escalated_at=None,
            closed_at=None,
        )


def test_evidence_and_scores_follow_contract_shape():
    evidence = FindingEvidence(
        evidence_id="EVIDENCE-000001",
        finding_id="FINDING-000001",
        source_type="CASE",
        source_id="CASE-000001",
        evidence_text="Case was marked high severity but escalation was not recorded.",
        observed_value=None,
        expected_value=None,
        created_at=datetime(2026, 1, 15, 13, 0, tzinfo=timezone.utc),
    )
    assert evidence.source_type == "CASE"

    score = SupervisoryScore(
        score_id="SCORE-000001",
        entity_id="ENTITY-0001",
        score=72.5,
        band="HIGH_ATTENTION",
        components={
            "execution_gap": 80.0,
            "negative_space": 60.0,
            "anomaly": 70.0,
            "peer_deviation": 75.0,
        },
        weights={
            "execution_gap": 0.30,
            "negative_space": 0.20,
            "anomaly": 0.25,
            "peer_deviation": 0.25,
        },
        calculated_at=datetime(2026, 1, 15, 13, 0, tzinfo=timezone.utc),
    )
    assert score.band == "HIGH_ATTENTION"
