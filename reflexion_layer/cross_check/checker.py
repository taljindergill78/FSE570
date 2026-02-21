"""Cross-check: compare findings across agents for consistency; flag conflicts."""

from __future__ import annotations

from collections import defaultdict
from typing import List

from osint_swarm.entities import Evidence

from reflexion_layer.cross_check.types import Conflict


def cross_check_findings(findings: List[Evidence]) -> List[Conflict]:
    """
    Compare findings for consistency. Flags conflicts when the same entity/date
    has materially different claims (e.g. different names or outcomes).
    """
    conflicts: List[Conflict] = []
    if not findings:
        return conflicts

    # Group by (entity_id, date) where date is non-empty
    by_entity_date: dict[tuple[str, str], List[Evidence]] = defaultdict(list)
    for e in findings:
        if e.date:
            by_entity_date[(e.entity_id, e.date)].append(e)

    for (entity_id, date), group in by_entity_date.items():
        if len(group) < 2:
            continue
        # Check for conflicting summaries (different key facts)
        summaries = [e.summary.strip() for e in group if e.summary]
        if len(set(summaries)) > 1:
            # Same entity+date but different summary text -> potential conflict
            ids = tuple(e.evidence_id for e in group[:5])  # cap for readability
            conflicts.append(
                Conflict(
                    dimension="summary_consistency",
                    evidence_ids=ids,
                    description=f"Same entity/date ({entity_id}, {date}) has differing summaries across {len(group)} findings.",
                )
            )

    return conflicts
