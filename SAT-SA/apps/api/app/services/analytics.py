from __future__ import annotations

from typing import Any

from app.services.validation import validate_records


def _score_record(record: dict[str, Any]) -> float:
    score = 0.0
    score += min(record.get("investigation_days", 0) / 10, 2.0)
    score += min(record.get("escalation_days", 0) / 10, 2.0)
    score += min(record.get("closure_days", 0) / 10, 2.0)
    score += min(record.get("backlog_count", 0) / 5, 2.0)
    return round(score, 2)


def run_analytics(records: list[dict[str, Any]]) -> dict[str, Any]:
    validation = validate_records(records)
    if not validation["valid"]:
        return {
            "valid": False,
            "errors": validation["errors"],
            "total_records": len(records),
            "findings": [],
            "summary": {"risk_level": "invalid", "count": 0},
        }

    findings: list[dict[str, Any]] = []
    for record in validation["records"]:
        score = _score_record(record)
        if record.get("investigation_days", 0) > 7 or record.get("backlog_count", 0) > 10:
            findings.append(
                {
                    "entity_id": record["entity_id"],
                    "case_id": record["case_id"],
                    "type": "execution_gap",
                    "score": score,
                    "evidence": {
                        "investigation_days": record.get("investigation_days"),
                        "backlog_count": record.get("backlog_count"),
                    },
                }
            )

    summary = {
        "risk_level": "moderate" if findings else "low",
        "count": len(findings),
        "avg_score": round(sum(item["score"] for item in findings) / len(findings), 2) if findings else 0.0,
    }

    return {
        "valid": True,
        "total_records": len(validation["records"]),
        "findings": findings,
        "summary": summary,
    }
