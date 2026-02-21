"""Tests for task planner (decomposition)."""

import pytest

from agents.lead_agent.task_planner import SubTask, decompose


def test_decompose_money_laundering_returns_five_tasks():
    tasks = decompose("Investigate Company X for money laundering red flags")
    assert len(tasks) == 5
    task_types = {t.task_type for t in tasks}
    assert "corporate_structure" in task_types
    assert "beneficial_ownership" in task_types
    assert "sanctions_screening" in task_types
    assert "transaction_patterns" in task_types
    assert "adverse_media" in task_types


def test_decompose_money_laundering_assigns_agents():
    tasks = decompose("Investigate for money laundering")
    agents = {t.target_agent for t in tasks}
    assert "corporate_agent" in agents
    assert "legal_agent" in agents
    assert "social_graph_agent" in agents


def test_decompose_generic_investigation_returns_default_tasks():
    tasks = decompose("Investigate Acme Corp")
    assert len(tasks) >= 1
    task_types = [t.task_type for t in tasks]
    assert "sec_filings" in task_types or "sanctions_screening" in task_types


def test_subtask_has_description():
    tasks = decompose("Investigate Tesla for money laundering")
    for t in tasks:
        assert t.task_type
        assert t.target_agent
        assert len(t.description) > 0


def test_decompose_aml_keyword_triggers_money_laundering():
    tasks = decompose("AML check for entity X")
    assert len(tasks) == 5
    assert any(t.task_type == "sanctions_screening" for t in tasks)
