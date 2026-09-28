from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


Severity = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
AlertStatus = Literal["OPEN", "ASSIGNED", "INVESTIGATING", "ESCALATED", "RESOLVED", "CLOSED"]
InvestigationStatus = Literal["NOT_STARTED", "IN_PROGRESS", "COMPLETED", "BLOCKED", "CANCELLED"]
FindingStatus = Literal["OPEN", "UNDER_REVIEW", "CONFIRMED", "DISMISSED", "RESOLVED"]
FindingPriority = Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
FindingType = Literal[
    "ESCALATION_EXECUTION_GAP",
    "INVESTIGATION_EXECUTION_GAP",
    "CLOSURE_EVIDENCE_GAP",
    "PROCESS_SEQUENCE_ANOMALY",
    "NEGATIVE_SPACE",
    "STATISTICAL_ANOMALY",
    "PEER_DEVIATION",
    "BACKLOG_ANOMALY",
]
ReviewActionType = Literal["CONFIRM", "DISMISS", "INVESTIGATE", "MARK_REVIEWED"]
AnalyticsRunStatus = Literal["QUEUED", "RUNNING", "COMPLETED", "FAILED"]
EvidenceSourceType = Literal["ALERT", "CASE", "INVESTIGATION", "ESCALATION", "ASSET", "ENTITY_METRIC", "PEER_METRIC"]


class Entity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entity_id: str
    entity_name: str
    entity_type: Literal["SOC"]
    sector: str | None = None
    peer_group: str
    active: bool


class Asset(BaseModel):
    model_config = ConfigDict(extra="forbid")

    asset_id: str
    entity_id: str
    asset_name: str
    asset_type: str
    criticality: str | None = None
    active: bool


class Analyst(BaseModel):
    model_config = ConfigDict(extra="forbid")

    analyst_id: str
    entity_id: str
    display_name: str
    active: bool


class Alert(BaseModel):
    model_config = ConfigDict(extra="forbid")

    alert_id: str
    entity_id: str
    timestamp: datetime
    alert_type: str
    severity: Severity
    asset_id: str
    status: AlertStatus
    assigned_to: str | None = None
    case_id: str | None = None


class Case(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    entity_id: str
    alert_id: str
    created_at: datetime
    assigned_at: datetime | None = None
    investigation_started: datetime | None = None
    investigation_completed: datetime | None = None
    escalated_at: datetime | None = None
    closed_at: datetime | None = None
    resolution: str | None = None
    closure_reason: str | None = None

    @model_validator(mode="after")
    def validate_case_timeline(self) -> "Case":
        timeline: list[tuple[str, datetime | None]] = [
            ("created_at", self.created_at),
            ("assigned_at", self.assigned_at),
            ("investigation_started", self.investigation_started),
            ("investigation_completed", self.investigation_completed),
            ("escalated_at", self.escalated_at),
            ("closed_at", self.closed_at),
        ]

        previous: datetime | None = None
        for field_name, value in timeline:
            if value is None:
                continue
            if previous is not None and value < previous:
                raise ValueError(f"{field_name} cannot precede the previous stage in the workflow")
            previous = value
        return self


class Investigation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    investigation_id: str
    case_id: str
    investigator: str
    started_at: datetime
    completed_at: datetime | None = None
    status: InvestigationStatus
    findings: str | None = None
    evidence_count: int | None = None

    @model_validator(mode="after")
    def validate_inv_duration(self) -> "Investigation":
        if self.completed_at is not None and self.completed_at < self.started_at:
            raise ValueError("investigation completion cannot precede investigation start")
        return self


class Escalation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    escalation_id: str
    case_id: str
    escalation_required: bool
    escalation_performed: bool
    escalation_level: str
    escalated_at: datetime | None = None

    @model_validator(mode="after")
    def validate_escalation(self) -> "Escalation":
        if self.escalated_at is not None and self.escalation_required and not self.escalation_performed:
            return self
        return self


class EntityMetric(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metric_id: str
    entity_id: str
    period_start: datetime
    period_end: datetime
    alert_count: int = Field(ge=0)
    high_severity_count: int = Field(ge=0)
    case_count: int = Field(ge=0)
    open_case_count: int = Field(ge=0)
    closed_case_count: int = Field(ge=0)
    escalation_required_count: int = Field(ge=0)
    escalation_performed_count: int = Field(ge=0)
    investigation_count: int = Field(ge=0)
    investigation_completed_count: int = Field(ge=0)
    average_investigation_minutes: float | None = None
    median_investigation_minutes: float | None = None
    backlog_count: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_metric_window(self) -> "EntityMetric":
        if self.period_end < self.period_start:
            raise ValueError("period_end cannot precede period_start")
        return self


class Finding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    finding_id: str
    entity_id: str
    finding_type: FindingType
    priority: FindingPriority
    status: FindingStatus
    title: str
    explanation: str
    expected_behavior: str
    observed_behavior: str
    detected_at: datetime
    metric_value: float | None = None
    metric_unit: str | None = None
    confidence: float | None = None


class FindingEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    evidence_id: str
    finding_id: str
    source_type: EvidenceSourceType
    source_id: str
    evidence_text: str
    observed_value: str | float | int | None = None
    expected_value: str | float | int | None = None
    created_at: datetime


class SupervisoryScore(BaseModel):
    model_config = ConfigDict(extra="forbid")

    score_id: str
    entity_id: str
    score: float
    band: str
    components: dict[str, float]
    weights: dict[str, float]
    calculated_at: datetime

    @model_validator(mode="after")
    def validate_weight_total(self) -> "SupervisoryScore":
        if self.weights:
            total = sum(self.weights.values())
            if abs(total - 1.0) > 0.0001:
                raise ValueError("weights must sum to 1.0 for the prototype configurable scoring model")
        return self


class ReviewAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    review_id: str
    finding_id: str
    reviewer_id: str
    action: ReviewActionType
    comment: str | None = None
    timestamp: datetime


class AnalyticsRun(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_id: str
    started_at: datetime
    completed_at: datetime | None = None
    status: AnalyticsRunStatus
    records_processed: int = Field(ge=0)
    findings_created: int = Field(ge=0)
    errors_count: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_run_timeline(self) -> "AnalyticsRun":
        if self.completed_at is not None and self.completed_at < self.started_at:
            raise ValueError("completed_at cannot precede started_at")
        return self


class AlertRecord(Alert):
    pass


class EntityRecord(Entity):
    pass


class AssetRecord(Asset):
    pass


class AnalystRecord(Analyst):
    pass
