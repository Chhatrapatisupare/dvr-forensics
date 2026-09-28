# SAT-SA

SAT-SA is a supervisory analytics MVP for periodic SOC-related operational data. It is designed for offline review and evidence-backed findings, not autonomous decision-making.

## Architecture

- FastAPI backend
- SQLite-ready persistence model
- deterministic synthetic dataset generation
- validation and analytics services
- evidence-backed findings and review metadata
- lightweight React + Vite frontend shell

## MVP Goals

- validate operational records
- generate deterministic synthetic SOC datasets
- compute supervisory analytics findings
- expose REST endpoints for health and analytics runs
- support human review and audit-friendly outputs

## Quick Start

```bash
python -m pip install -e .[dev]
pytest
```

## Notes

This is intentionally an offline, minimal, audit-friendly implementation suitable for a solo-developer MVP.
