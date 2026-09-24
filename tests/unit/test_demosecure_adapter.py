from pathlib import Path

from packages.adapters.demosecure import DemoSecureAdapter
from packages.adapters.registry import AdapterRegistry


FIXTURE = Path("fixtures/demo_dvr/demo_dvr.img")


def test_demosecure_detection():
    adapter = DemoSecureAdapter()

    assert adapter.detect(FIXTURE) is True


def test_demosecure_inspection():
    adapter = DemoSecureAdapter()

    metadata = adapter.inspect(FIXTURE)

    assert metadata["vendor"] == "DemoSecure"
    assert metadata["model"] == "DS-NVR-8000"
    assert metadata["filesystem"] == "DemoFS"


def test_recording_discovery():
    adapter = DemoSecureAdapter()

    recordings = adapter.list_recordings(FIXTURE)

    assert len(recordings) == 3
    assert recordings[0]["id"] == "REC-001"
    assert recordings[2]["status"] == "recovered"


def test_adapter_registry():
    registry = AdapterRegistry()

    adapter = registry.detect(FIXTURE)

    assert adapter is not None
    assert adapter.name == "DemoSecure"
    