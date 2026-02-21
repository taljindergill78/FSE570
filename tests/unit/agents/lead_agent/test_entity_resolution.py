"""Tests for entity resolution."""

import pytest

from agents.lead_agent.entity_resolution import resolve, resolve_one
from osint_swarm.entities import Entity


def test_resolve_empty_returns_empty():
    assert resolve("") == []
    assert resolve("   ") == []


def test_resolve_tesla_by_name():
    candidates = resolve("Tesla")
    assert len(candidates) >= 1
    assert candidates[0].entity_id == "tesla_inc_cik_0001318605"
    assert "0001318605" in candidates[0].identifiers.get("cik", "")


def test_resolve_tesla_case_insensitive():
    assert resolve_one("tesla") is not None
    assert resolve_one("TESLA") is not None
    assert resolve_one("Tesla, Inc.") is not None


def test_resolve_one_returns_first_match():
    entity = resolve_one("Tesla")
    assert entity is not None
    assert entity.name == "Tesla, Inc."


def test_resolve_one_unknown_returns_none():
    assert resolve_one("Unknown Company XYZ") is None


def test_resolve_by_alias():
    # Tesla has alias "Tesla Motors"
    entity = resolve_one("Tesla Motors")
    assert entity is not None
    assert entity.entity_id == "tesla_inc_cik_0001318605"
