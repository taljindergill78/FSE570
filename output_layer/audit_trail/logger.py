"""Audit trail: log queries, data sources, and reasoning steps for chain of custody."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class AuditTrail:
    """
    Append-only log of investigation steps: query, entity resolution, task dispatch,
    data sources accessed, reflexion steps. Export to JSON for chain of custody.
    """

    events: List[Dict[str, Any]] = field(default_factory=list)

    def record(self, step_type: str, **payload: Any) -> None:
        """Append one event with timestamp and step type."""
        self.events.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "step": step_type,
            **payload,
        })

    def get_events(self) -> List[Dict[str, Any]]:
        """Return a copy of all events."""
        return [dict(e) for e in self.events]

    def to_json_lines(self) -> str:
        """One JSON object per line (JSON Lines format) for append-friendly logging."""
        return "\n".join(json.dumps(e, default=str) for e in self.events)

    def clear(self) -> None:
        """Clear all events (e.g. for a new investigation)."""
        self.events.clear()
