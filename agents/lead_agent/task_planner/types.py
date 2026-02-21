"""Task types for decomposition."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SubTask:
    """A single sub-task allocated to a specialist agent."""

    task_type: str
    target_agent: str
    description: str
