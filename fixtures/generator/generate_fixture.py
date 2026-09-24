from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = ROOT / "fixtures" / "demo_dvr"
IMAGE_PATH = FIXTURE_DIR / "demo_dvr.img"
MANIFEST_PATH = FIXTURE_DIR / "manifest.json"


def create_fixture() -> None:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)

    recordings = [
        {
            "id": "REC-001",
            "camera": "CAM-01",
            "channel": 1,
            "start_time": "2026-09-20T09:00:00Z",
            "end_time": "2026-09-20T09:05:00Z",
            "status": "normal",
            "format": "MP4",
        },
        {
            "id": "REC-002",
            "camera": "CAM-02",
            "channel": 2,
            "start_time": "2026-09-20T09:10:00Z",
            "end_time": "2026-09-20T09:15:00Z",
            "status": "normal",
            "format": "MP4",
        },
        {
            "id": "REC-003",
            "camera": "CAM-01",
            "channel": 1,
            "start_time": "2026-09-20T09:20:00Z",
            "end_time": "2026-09-20T09:25:00Z",
            "status": "recovered",
            "format": "MP4",
        },
    ]

    metadata = {
        "magic": "DEMOSECURE-DVR-IMAGE",
        "vendor": "DemoSecure",
        "model": "DS-NVR-8000",
        "firmware": "1.4.2-demo",
        "timezone": "UTC",
        "filesystem": "DemoFS",
        "channels": 8,
        "recordings": recordings,
    }

    payload = (
        "=== DEMOSECURE FORENSIC FIXTURE ===\n"
        + json.dumps(metadata, indent=2)
        + "\n=== END DEMOSECURE FIXTURE ===\n"
    ).encode("utf-8")

    IMAGE_PATH.write_bytes(payload)

    MANIFEST_PATH.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    print(f"Created: {IMAGE_PATH}")
    print(f"Manifest: {MANIFEST_PATH}")
    print(f"Size: {IMAGE_PATH.stat().st_size} bytes")


if __name__ == "__main__":
    create_fixture()
    