from __future__ import annotations

from pathlib import Path

from packages.adapters.base import VendorAdapter
from packages.adapters.demosecure import DemoSecureAdapter


class AdapterRegistry:
    """
    Registry responsible for selecting the appropriate
    vendor adapter for an evidence source.
    """

    def __init__(self) -> None:
        self.adapters: list[VendorAdapter] = [
            DemoSecureAdapter(),
        ]

    def register(self, adapter: VendorAdapter) -> None:
        self.adapters.append(adapter)

    def detect(self, evidence_path: Path) -> VendorAdapter | None:
        for adapter in self.adapters:
            if adapter.detect(evidence_path):
                return adapter

        return None