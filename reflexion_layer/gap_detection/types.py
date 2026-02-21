"""Types for gap detection results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Gap:
    """A missing piece in the investigation (e.g. no sanctions data)."""

    area: str
    description: str
    suggested_follow_up: Optional[str] = None
