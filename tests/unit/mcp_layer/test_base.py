"""Tests for MCP layer base interface."""

import pytest

from mcp_layer.base import DataSourceProcessor
from osint_swarm.entities import Entity, Evidence


class DummyProcessor(DataSourceProcessor):
    """Concrete processor for testing the interface."""

    @property
    def source_id(self) -> str:
        return "dummy"

    def get_evidence_for_entity(self, entity: Entity) -> list[Evidence]:
        return [
            Evidence(
                evidence_id="dummy_1",
                entity_id=entity.entity_id,
                date="2024-01-01",
                source_type="other",
                risk_category="other",
                summary="Dummy",
                source_uri="https://example.com",
                confidence=0.5,
            )
        ]


def test_data_source_processor_interface():
    """DataSourceProcessor has source_id and get_evidence_for_entity."""
    proc = DummyProcessor()
    assert proc.source_id == "dummy"
    entity = Entity(entity_id="test_entity", name="Test")
    evidence = proc.get_evidence_for_entity(entity)
    assert len(evidence) == 1
    assert evidence[0].evidence_id == "dummy_1"
    assert evidence[0].entity_id == "test_entity"
