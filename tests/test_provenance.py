from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
API_PATH = PROJECT_ROOT / "apps" / "api"

sys.path.insert(0, str(API_PATH))

from app.database import SessionLocal
from app.services.provenance_service import ProvenanceService


EVIDENCE_ID = "EVIDENCE-C92B2AADB8F1"


def test_provenance_contains_evidence_node():
    db = SessionLocal()

    try:
        graph = ProvenanceService().build_graph(
            db=db,
            evidence_id=EVIDENCE_ID,
        )

        evidence_nodes = [
            node
            for node in graph["nodes"]
            if node["type"] == "evidence"
        ]

        assert len(evidence_nodes) == 1
        assert evidence_nodes[0]["id"] == EVIDENCE_ID

    finally:
        db.close()


def test_provenance_contains_recordings():
    db = SessionLocal()

    try:
        graph = ProvenanceService().build_graph(
            db=db,
            evidence_id=EVIDENCE_ID,
        )

        recording_ids = {
            node["id"]
            for node in graph["nodes"]
            if node["type"] == "recording"
        }

        assert {
            "REC-001",
            "REC-002",
            "REC-003",
        }.issubset(recording_ids)

    finally:
        db.close()


def test_provenance_links_evidence_to_recordings():
    db = SessionLocal()

    try:
        graph = ProvenanceService().build_graph(
            db=db,
            evidence_id=EVIDENCE_ID,
        )

        contains_edges = [
            edge
            for edge in graph["edges"]
            if edge["relationship"] == "CONTAINS"
        ]

        assert len(contains_edges) == 3

        targets = {
            edge["target"]
            for edge in contains_edges
        }

        assert targets == {
            "REC-001",
            "REC-002",
            "REC-003",
        }

    finally:
        db.close()


def test_provenance_links_recovered_artifact():
    db = SessionLocal()

    try:
        graph = ProvenanceService().build_graph(
            db=db,
            evidence_id=EVIDENCE_ID,
        )

        artifact_nodes = [
            node
            for node in graph["nodes"]
            if node["type"] == "artifact"
        ]

        assert len(artifact_nodes) >= 1

        artifact = next(
            node
            for node in artifact_nodes
            if node["metadata"]["recording_id"] == "REC-003"
        )

        recovery_edges = [
            edge
            for edge in graph["edges"]
            if (
                edge["relationship"] == "RECOVERED_AS"
                and edge["source"] == "REC-003"
                and edge["target"] == artifact["id"]
            )
        ]

        assert len(recovery_edges) == 1

    finally:
        db.close()