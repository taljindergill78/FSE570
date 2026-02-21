"""Gap detection: identify missing information from investigation context."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from reflexion_layer.gap_detection.types import Gap

if TYPE_CHECKING:
    from agents.lead_agent.context_manager import InvestigationContext


def detect_gaps(context: "InvestigationContext") -> List[Gap]:
    """
    Given investigation objectives and current findings, list missing pieces.
    E.g. agents that returned only stub evidence -> gap in that area.
    """
    gaps: List[Gap] = []
    if not context.get_entity():
        gaps.append(
            Gap(
                area="entity_resolution",
                description="No entity resolved from query.",
                suggested_follow_up="Rephrase query with a known entity name or identifier.",
            )
        )
        return gaps

    # Check each agent's results for stub-only output
    stub_agents = {
        "legal_agent": ("Sanctions / legal", "Sanctions screening and PACER not yet integrated.", "Add OFAC/sanctions list or CourtListener integration."),
        "social_graph_agent": ("Adverse media / network", "Social graph and adverse media not yet integrated.", "Add Twitter/LinkedIn or GDELT integration."),
    }
    for agent_id, (area, desc, follow_up) in stub_agents.items():
        results = context.get_agent_results(agent_id)
        if not results:
            gaps.append(Gap(area=area, description=f"{desc} No findings returned.", suggested_follow_up=follow_up))
        elif all(getattr(e, "attributes", {}).get("stub") for e in results):
            gaps.append(Gap(area=area, description=f"{desc} Only stub placeholders returned.", suggested_follow_up=follow_up))

    # Corporate beneficial_ownership: if structure_mapper stub was returned, that area is missing
    corp_results = context.get_agent_results("corporate_agent")
    if any("structure_mapper" in e.evidence_id and e.attributes.get("stub") for e in corp_results):
        gaps.append(
            Gap(
                area="beneficial_ownership",
                description="Beneficial ownership / structure mapping not yet integrated (OpenCorporates planned).",
                suggested_follow_up="Integrate OpenCorporates API for corporate network data.",
            )
        )

    return gaps
