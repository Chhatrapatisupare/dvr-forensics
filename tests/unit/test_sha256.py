import hashlib
from packages.forensics.hashing.sha256 import calculate_sha256


def test_sha256_calculation(tmp_path):
    evidence_file = tmp_path / "sample.bin"
    evidence_file.write_bytes(b"SIH26150-DVR-FORENSICS")

    expected = hashlib.sha256(
        b"SIH26150-DVR-FORENSICS"
    ).hexdigest()

    assert calculate_sha256(evidence_file) == expected