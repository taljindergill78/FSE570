"""Tests for output_layer audit trail."""

import json
import pytest

from output_layer.audit_trail import AuditTrail


def test_audit_trail_starts_empty():
    trail = AuditTrail()
    assert trail.get_events() == []
    assert trail.to_json_lines() == ""


def test_audit_trail_record_appends_event():
    trail = AuditTrail()
    trail.record("query_received", query="Investigate Tesla")
    events = trail.get_events()
    assert len(events) == 1
    assert events[0]["step"] == "query_received"
    assert events[0]["query"] == "Investigate Tesla"
    assert "timestamp" in events[0]


def test_audit_trail_multiple_events():
    trail = AuditTrail()
    trail.record("entity_resolved", entity_id="tesla_inc_cik_0001318605")
    trail.record("task_dispatched", task_type="corporate_structure", agent_id="corporate_agent")
    events = trail.get_events()
    assert len(events) == 2
    assert events[0]["step"] == "entity_resolved"
    assert events[1]["step"] == "task_dispatched"
    assert events[1]["task_type"] == "corporate_structure"


def test_audit_trail_to_json_lines():
    trail = AuditTrail()
    trail.record("query_received", query="Test")
    lines = trail.to_json_lines()
    assert "\n" not in lines or lines.count("\n") == 0  # one line for one event
    parsed = json.loads(lines)
    assert parsed["step"] == "query_received"
    assert parsed["query"] == "Test"


def test_audit_trail_clear():
    trail = AuditTrail()
    trail.record("query_received", query="Test")
    trail.clear()
    assert trail.get_events() == []
    assert trail.to_json_lines() == ""
