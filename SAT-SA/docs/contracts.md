# SAT-SA Domain & Data Contracts

This document defines the canonical contract for the SAT-SA MVP. The design is intentionally contract-first: the database model, Pydantic schemas, service layer, API layer, and frontend types must all share the same domain vocabulary.

## Contract Principles

- Identifiers are strings.
- Timestamps are ISO 8601 UTC timestamps.
- Missing optional values are represented as `null`, never `""`, `"N/A"`, `"unknown"`, or similar placeholders.
- Every analytical finding is a supervisory signal, not proof of wrongdoing.
- The scoring model is explicitly labelled as a prototype configurable model.

## Canonical flow

```text
Domain Contract
  ↓
Database Model
  ↓
Pydantic Schema
  ↓
Service
  ↓
API
  ↓
Frontend Type
```

## Domain objects

### Entity

```json
{
  "entity_id": "ENTITY-0001",
  "entity_name": "SOC Alpha",
  "entity_type": "SOC",
  "sector": "Government",
  "peer_group": "TIER_1",
  "active": true
}
```

### Asset

```json
{
  "asset_id": "ASSET-0001",
  "entity_id": "ENTITY-0001",
  "asset_name": "Application Server 01",
  "asset_type": "SERVER",
  "criticality": "HIGH",
  "active": true
}
```

### Analyst

```json
{
  "analyst_id": "ANALYST-0001",
  "entity_id": "ENTITY-0001",
  "display_name": "Analyst 01",
  "active": true
}
```

### Alert

```json
{
  "alert_id": "ALERT-000001",
  "entity_id": "ENTITY-0001",
  "timestamp": "2026-01-15T09:30:00Z",
  "alert_type": "SUSPICIOUS_LOGIN",
  "severity": "HIGH",
  "asset_id": "ASSET-0001",
  "status": "OPEN",
  "assigned_to": null,
  "case_id": null
}
```

### Case

```json
{
  "case_id": "CASE-000001",
  "entity_id": "ENTITY-0001",
  "alert_id": "ALERT-000001",
  "created_at": "2026-01-15T09:35:00Z",
  "assigned_at": "2026-01-15T09:40:00Z",
  "investigation_started": "2026-01-15T09:50:00Z",
  "investigation_completed": "2026-01-15T11:10:00Z",
  "escalated_at": null,
  "closed_at": "2026-01-15T12:00:00Z",
  "resolution": "Benign activity",
  "closure_reason": "Verified by analyst"
}
```

### Investigation

```json
{
  "investigation_id": "INV-000001",
  "case_id": "CASE-000001",
  "investigator": "ANALYST-0001",
  "started_at": "2026-01-15T09:50:00Z",
  "completed_at": "2026-01-15T11:10:00Z",
  "status": "COMPLETED",
  "findings": "Activity verified",
  "evidence_count": 3
}
```

### Escalation

```json
{
  "escalation_id": "ESC-000001",
  "case_id": "CASE-000001",
  "escalation_required": true,
  "escalation_performed": false,
  "escalation_level": "LEVEL_2",
  "escalated_at": null
}
```

Important: if `escalation_required = true` and `escalation_performed = false`, the analytics engine may generate an execution-gap finding. This is an analytical signal that requires human review.

### Entity Metrics

```json
{
  "metric_id": "METRIC-000001",
  "entity_id": "ENTITY-0001",
  "period_start": "2026-01-01T00:00:00Z",
  "period_end": "2026-01-31T23:59:59Z",
  "alert_count": 125,
  "high_severity_count": 32,
  "case_count": 81,
  "open_case_count": 13,
  "closed_case_count": 68,
  "escalation_required_count": 15,
  "escalation_performed_count": 13,
  "investigation_count": 74,
  "investigation_completed_count": 70,
  "average_investigation_minutes": 94.5,
  "median_investigation_minutes": 71.0,
  "backlog_count": 13
}
```

### Finding

```json
{
  "finding_id": "FINDING-000001",
  "entity_id": "ENTITY-0001",
  "finding_type": "ESCALATION_EXECUTION_GAP",
  "priority": "HIGH",
  "status": "OPEN",
  "title": "Required escalation not recorded",
  "explanation": "A high-severity workflow required escalation, but no escalation event was recorded.",
  "expected_behavior": "Required escalation should be recorded.",
  "observed_behavior": "No escalation event was recorded.",
  "detected_at": "2026-01-15T13:00:00Z",
  "metric_value": null,
  "metric_unit": null,
  "confidence": null
}
```

### Finding Evidence

```json
{
  "evidence_id": "EVIDENCE-000001",
  "finding_id": "FINDING-000001",
  "source_type": "CASE",
  "source_id": "CASE-000001",
  "evidence_text": "Case was marked high severity but escalation was not recorded.",
  "observed_value": null,
  "expected_value": null,
  "created_at": "2026-01-15T13:00:00Z"
}
```

### Supervisory Score

```json
{
  "score_id": "SCORE-000001",
  "entity_id": "ENTITY-0001",
  "score": 72.5,
  "band": "HIGH_ATTENTION",
  "components": {
    "execution_gap": 80.0,
    "negative_space": 60.0,
    "anomaly": 70.0,
    "peer_deviation": 75.0
  },
  "weights": {
    "execution_gap": 0.30,
    "negative_space": 0.20,
    "anomaly": 0.25,
    "peer_deviation": 0.25
  },
  "calculated_at": "2026-01-15T13:00:00Z"
}
```

The scoring model must be explicitly labelled as a Prototype Configurable Scoring Model. It is not an official NTRO scoring formula.

### Review Action

```json
{
  "review_id": "REVIEW-000001",
  "finding_id": "FINDING-000001",
  "reviewer_id": "REVIEWER-0001",
  "action": "INVESTIGATE",
  "comment": "Requires manual verification.",
  "timestamp": "2026-01-15T13:15:00Z"
}
```

### Analytics Run

```json
{
  "run_id": "RUN-000001",
  "started_at": "2026-01-15T13:00:00Z",
  "completed_at": "2026-01-15T13:01:32Z",
  "status": "COMPLETED",
  "records_processed": 10000,
  "findings_created": 42,
  "errors_count": 0
}
```

## Enumerations

### Severity

```text
LOW
MEDIUM
HIGH
CRITICAL
```

### Alert status

```text
OPEN
ASSIGNED
INVESTIGATING
ESCALATED
RESOLVED
CLOSED
```

### Investigation status

```text
NOT_STARTED
IN_PROGRESS
COMPLETED
BLOCKED
CANCELLED
```

### Finding status

```text
OPEN
UNDER_REVIEW
CONFIRMED
DISMISSED
RESOLVED
```

### Finding priority

```text
LOW
MEDIUM
HIGH
CRITICAL
```

### Finding type

```text
ESCALATION_EXECUTION_GAP
INVESTIGATION_EXECUTION_GAP
CLOSURE_EVIDENCE_GAP
PROCESS_SEQUENCE_ANOMALY
NEGATIVE_SPACE
STATISTICAL_ANOMALY
PEER_DEVIATION
BACKLOG_ANOMALY
```

### Review action

```text
CONFIRM
DISMISS
INVESTIGATE
MARK_REVIEWED
```

### Analytics run status

```text
QUEUED
RUNNING
COMPLETED
FAILED
```

## Identifier Rules

Identifiers must be deterministic and human-readable. Examples:

```text
ENTITY-0001
ASSET-0001
ANALYST-0001
ALERT-000001
CASE-000001
INV-000001
ESC-000001
FINDING-000001
EVIDENCE-000001
REVIEW-000001
RUN-000001
```

## Timestamp Rules

- All timestamps are UTC.
- Backend logic must not mix timezone-aware and timezone-naive datetime values.
- Timestamps must be stored in ISO 8601 UTC form: `2026-01-15T09:30:00Z`.

## Missing Data Rules

Missing values are represented as `null`. Never use empty strings or placeholder text.

## Contract Invariants

The implementation must validate the following:

1. IDs are present and correctly formatted.
2. Foreign-key relationships are valid.
3. Enum values are valid.
4. Required fields are present.
5. Timestamps are valid.
6. Case timestamps do not occur out of sequence.
7. Investigation completion cannot precede investigation start.
8. Escalation time cannot precede case creation.
9. Closure cannot precede case creation.
10. Review actions reference an existing finding.
11. Finding evidence references an existing finding.
12. Analytics runs have valid statuses.
13. Rates remain between 0 and 1.
14. Counts cannot be negative.

## Contract-first implementation rule

The canonical domain model must be the single source of truth. Changes to canonical fields must be deliberate and propagated through all layers without creating competing names for the same concept.
