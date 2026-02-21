"""Evidence report generator: human-readable report with citations and confidence."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple

from osint_swarm.entities import Evidence

from knowledge_graph.types import Edge, Node


def generate_markdown_report(
    findings: List[Evidence],
    entity_id: Optional[str] = None,
    query: str = "",
    graph: Optional[Tuple[List[Node], List[Edge]]] = None,
) -> str:
    """
    Produce a Markdown report from evidence (and optional knowledge graph).
    Sections: title, query/entity, findings by risk category, source citations, optional graph summary.
    """
    lines: List[str] = []
    lines.append("# Investigation Evidence Report")
    lines.append("")
    if query:
        lines.append(f"**Query:** {query}")
        lines.append("")
    if entity_id:
        lines.append(f"**Entity:** `{entity_id}`")
        lines.append("")
    lines.append(f"**Total findings:** {len(findings)}")
    lines.append("")

    # By risk category
    by_risk: dict[str, List[Evidence]] = {}
    for e in findings:
        by_risk.setdefault(e.risk_category, []).append(e)
    for risk in ["governance", "regulatory", "legal", "network", "other"]:
        if risk not in by_risk:
            continue
        lines.append(f"## {risk.replace('_', ' ').title()}")
        lines.append("")
        for e in by_risk[risk]:
            lines.append(f"- **{e.summary[:200]}{'...' if len(e.summary) > 200 else ''}**")
            lines.append(f"  - Date: {e.date or 'N/A'} | Confidence: {e.confidence:.2f}")
            if e.source_uri:
                lines.append(f"  - Source: [{e.source_uri}]({e.source_uri})")
            lines.append("")
        lines.append("")

    if graph:
        nodes, edges = graph
        lines.append("## Knowledge Graph Summary")
        lines.append("")
        lines.append(f"- Nodes: {len(nodes)} (entities: {sum(1 for n in nodes if n.node_type == 'entity')}, evidence: {sum(1 for n in nodes if n.node_type == 'evidence')})")
        lines.append(f"- Edges: {len(edges)}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def write_markdown_report(
    path: Path,
    findings: List[Evidence],
    entity_id: Optional[str] = None,
    query: str = "",
    graph: Optional[Tuple[List[Node], List[Edge]]] = None,
) -> None:
    """Generate Markdown report and write to file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        generate_markdown_report(findings, entity_id=entity_id, query=query, graph=graph),
        encoding="utf-8",
    )


def generate_html_report(
    findings: List[Evidence],
    entity_id: Optional[str] = None,
    query: str = "",
    graph: Optional[Tuple[List[Node], List[Edge]]] = None,
) -> str:
    """Produce an HTML report (simple, with citations and confidence)."""
    body_parts: List[str] = []
    body_parts.append("<h1>Investigation Evidence Report</h1>")
    if query:
        body_parts.append(f"<p><strong>Query:</strong> {query}</p>")
    if entity_id:
        body_parts.append(f"<p><strong>Entity:</strong> <code>{entity_id}</code></p>")
    body_parts.append(f"<p><strong>Total findings:</strong> {len(findings)}</p>")

    by_risk: dict[str, List[Evidence]] = {}
    for e in findings:
        by_risk.setdefault(e.risk_category, []).append(e)
    for risk in ["governance", "regulatory", "legal", "network", "other"]:
        if risk not in by_risk:
            continue
        body_parts.append(f"<h2>{risk.replace('_', ' ').title()}</h2>")
        body_parts.append("<ul>")
        for e in by_risk[risk]:
            summary_esc = e.summary[:200].replace("<", "&lt;").replace(">", "&gt;")
            if len(e.summary) > 200:
                summary_esc += "..."
            body_parts.append(f"<li><strong>{summary_esc}</strong><br>Date: {e.date or 'N/A'} | Confidence: {e.confidence:.2f}")
            if e.source_uri:
                body_parts.append(f'<br><a href="{e.source_uri}">Source</a>')
            body_parts.append("</li>")
        body_parts.append("</ul>")

    if graph:
        nodes, edges = graph
        n_entity = sum(1 for n in nodes if n.node_type == "entity")
        n_evidence = sum(1 for n in nodes if n.node_type == "evidence")
        body_parts.append("<h2>Knowledge Graph Summary</h2>")
        body_parts.append(f"<p>Nodes: {len(nodes)} (entities: {n_entity}, evidence: {n_evidence}) | Edges: {len(edges)}</p>")

    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Evidence Report</title></head><body>"
        + "\n".join(body_parts)
        + "</body></html>"
    )
