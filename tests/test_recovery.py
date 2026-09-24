from pathlib import Path

from apps.api.app.services.recovery_service import RecoveryService
from packages.forensics.hashing.sha256 import calculate_sha256


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EVIDENCE_PATH = (
    PROJECT_ROOT
    / "fixtures"
    / "demo_dvr"
    / "demo_dvr.img"
)

EVIDENCE_ID = "EVIDENCE-C92B2AADB8F1"
RECORDING_ID = "REC-003"

EXPECTED_SOURCE_HASH = (
    "b7cf9ff5ce94bb60df8bf56548b17db8bf3a543288d76ad3e06a2f3460d88f5c"
)


def test_recovery_does_not_modify_source(tmp_path):
    before_hash = calculate_sha256(EVIDENCE_PATH)

    artifact = RecoveryService().recover_recording(
        evidence_id=EVIDENCE_ID,
        evidence_path=str(EVIDENCE_PATH),
        recording_id=RECORDING_ID,
        output_directory=tmp_path,
    )

    after_hash = calculate_sha256(EVIDENCE_PATH)

    assert before_hash == EXPECTED_SOURCE_HASH
    assert after_hash == EXPECTED_SOURCE_HASH
    assert artifact.status == "RECOVERED"
    assert artifact.confidence == "DEMO"


def test_recovery_artifact_exists_and_has_hash(tmp_path):
    artifact = RecoveryService().recover_recording(
        evidence_id=EVIDENCE_ID,
        evidence_path=str(EVIDENCE_PATH),
        recording_id=RECORDING_ID,
        output_directory=tmp_path,
    )

    artifact_path = Path(artifact.output_path)

    assert artifact_path.exists()
    assert artifact_path.is_file()
    assert artifact.size_bytes == artifact_path.stat().st_size
    assert calculate_sha256(artifact_path) == artifact.sha256


def test_recovery_artifact_contains_recording_metadata(tmp_path):
    artifact = RecoveryService().recover_recording(
        evidence_id=EVIDENCE_ID,
        evidence_path=str(EVIDENCE_PATH),
        recording_id=RECORDING_ID,
        output_directory=tmp_path,
    )

    content = Path(artifact.output_path).read_text(encoding="utf-8")

    assert "SYNTHETIC RECOVERY" in content
    assert RECORDING_ID in content
    assert EVIDENCE_ID in content
    assert "DemoSecure synthetic recovery" in content