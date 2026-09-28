from __future__ import annotations

from typing import Any

VALID_STATUSES = {"OPEN", "IN_PROGRESS", "ESCALATED", "CLOSED"}
VALID_PEER_GROUPS = {"GROUP_1", "GROUP_2", "GROUP_3", "GROUP_4"}


def validate_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    valid_records: list[dict[str, Any]] = []

    for index, record in enumerate(records):
        required_fields = [
            "entity_id",
            "case_id",
            "timestamp",
            "status",
            "investigation_days",
            "escalation_days",
            "closure_days",
            "backlog_count",
            "peer_group",
            "profile",
        ]
        missing = [field for field in required_fields if field not in record]
        if missing:
            errors.append(f"Record {index}: missing {missing}")
            continue

        if record["status"] not in VALID_STATUSES:
            errors.append(f"Record {index}: unsupported status {record['status']}")

        if record["peer_group"] not in VALID_PEER_GROUPS:
            errors.append(f"Record {index}: unsupported peer group {record['peer_group']}")

        for field in ["investigation_days", "escalation_days", "closure_days", "backlog_count"]:
            if not isinstance(record[field], int):
                errors.append(f"Record {index}: field {field} must be int")
                break

        if record["investigation_days"] < 0 or record["escalation_days"] < 0 or record["closure_days"] < 0 or record["backlog_count"] < 0:
            errors.append(f"Record {index}: negative values not allowed")

        valid_records.append(record)

    return {"valid": not errors, "records": valid_records, "errors": errors}
