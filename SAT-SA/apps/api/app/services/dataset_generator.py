from __future__ import annotations

import random
from typing import Any

PROFILE_DEFS = {
    "NORMAL": {
        "investigation_days": (1, 4),
        "escalation_days": (1, 3),
        "closure_days": (2, 6),
        "backlog_count": (0, 2),
    },
    "SLOW_INVESTIGATION": {
        "investigation_days": (8, 18),
        "escalation_days": (2, 5),
        "closure_days": (5, 12),
        "backlog_count": (3, 8),
    },
    "ESCALATION_GAP": {
        "investigation_days": (2, 6),
        "escalation_days": (7, 15),
        "closure_days": (3, 9),
        "backlog_count": (2, 7),
    },
    "CLOSURE_GAP": {
        "investigation_days": (2, 5),
        "escalation_days": (2, 5),
        "closure_days": (12, 25),
        "backlog_count": (4, 10),
    },
    "HIGH_BACKLOG": {
        "investigation_days": (3, 7),
        "escalation_days": (2, 6),
        "closure_days": (5, 15),
        "backlog_count": (12, 35),
    },
    "MIXED": {
        "investigation_days": (2, 14),
        "escalation_days": (2, 14),
        "closure_days": (3, 18),
        "backlog_count": (1, 18),
    },
}


VALID_STATUS_SEQUENCE = ["OPEN", "IN_PROGRESS", "ESCALATED", "CLOSED"]


def generate_dataset(profile: str, seed: int = 42, size: int = 30) -> list[dict[str, Any]]:
    if profile not in PROFILE_DEFS:
        raise ValueError(f"Unsupported profile: {profile}")

    rng = random.Random(seed)
    profile_cfg = PROFILE_DEFS[profile]
    records: list[dict[str, Any]] = []

    for i in range(size):
        investigation_days = rng.randint(*profile_cfg["investigation_days"])
        escalation_days = rng.randint(*profile_cfg["escalation_days"])
        closure_days = rng.randint(*profile_cfg["closure_days"])
        backlog_count = rng.randint(*profile_cfg["backlog_count"])
        status = VALID_STATUS_SEQUENCE[i % len(VALID_STATUS_SEQUENCE)]
        entity_id = f"E-{(i % 12) + 1:03d}"
        case_id = f"C-{i + 1:04d}"

        records.append(
            {
                "entity_id": entity_id,
                "case_id": case_id,
                "timestamp": f"2025-01-{(i % 28) + 1:02d}T00:00:00",
                "status": status,
                "investigation_days": investigation_days,
                "escalation_days": escalation_days,
                "closure_days": closure_days,
                "backlog_count": backlog_count,
                "peer_group": f"GROUP_{(i % 4) + 1}",
                "profile": profile,
            }
        )

    return records
