"""Full investigation pipeline: Lead Agent -> reflexion -> knowledge graph -> report -> dashboard -> audit."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

# Path setup for running as app
import sys
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for p in (ROOT, SRC):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from agents.lead_agent import LeadAgent
from knowledge_graph import build_graph_from_evidence
from output_layer.audit_trail import AuditTrail
from output_layer.evidence_report_generator import generate_markdown_report
from output_layer.risk_dashboard import compute_risk_scores, format_dashboard_cli
from reflexion_layer import aggregate_confidence, cross_check_findings, detect_gaps


def run_investigation(query: str, data_root: Optional[Path] = None) -> Dict[str, Any]:
    """
    Run the full pipeline for one investigation query.
    Returns a dict with keys: query, entity, tasks, findings_count, findings_by_agent,
    report_md, report_html, risk_scores, risk_dashboard_cli, gaps, conflicts,
    confidence_scores, audit_events, error (if any).
    """
    data_root = data_root or ROOT / "data"
    audit = AuditTrail()
    result: Dict[str, Any] = {
        "query": query,
        "entity": None,
        "entity_id": None,
        "entity_name": None,
        "tasks": [],
        "findings_count": 0,
        "findings_by_agent": {},
        "report_md": "",
        "report_html": "",
        "risk_scores": None,
        "risk_dashboard_cli": "",
        "gaps": [],
        "conflicts": [],
        "confidence_scores": None,
        "audit_events": [],
        "error": None,
    }

    try:
        audit.record("query_received", query=query)
        agent = LeadAgent(data_root=data_root)
        ctx = agent.run(query)
        audit.record("pipeline_completed", entity_resolved=ctx.get_entity() is not None, task_count=len(ctx.get_tasks()))

        entity = ctx.get_entity()
        if entity:
            result["entity_id"] = entity.entity_id
            result["entity_name"] = entity.name
            result["entity"] = {"entity_id": entity.entity_id, "name": entity.name, "identifiers": dict(entity.identifiers)}

        result["tasks"] = [{"task_type": t.task_type, "target_agent": t.target_agent, "description": t.description} for t in ctx.get_tasks()]
        findings = ctx.get_all_findings()
        result["findings_count"] = len(findings)
        result["findings_by_agent"] = {aid: len(evs) for aid, evs in ctx.results.items()}

        # Reflexion
        result["conflicts"] = [{"dimension": c.dimension, "description": c.description, "evidence_ids": list(c.evidence_ids)} for c in cross_check_findings(findings)]
        result["gaps"] = [{"area": g.area, "description": g.description, "suggested_follow_up": g.suggested_follow_up} for g in detect_gaps(ctx)]
        conf_scores = aggregate_confidence(findings)
        result["confidence_scores"] = {"overall": conf_scores.overall, "by_risk_category": conf_scores.by_risk_category, "by_source_type": conf_scores.by_source_type}

        # Knowledge graph
        nodes, edges = build_graph_from_evidence(findings)
        result["graph_summary"] = {"nodes": len(nodes), "edges": len(edges), "entity_nodes": sum(1 for n in nodes if n.node_type == "entity"), "evidence_nodes": sum(1 for n in nodes if n.node_type == "evidence")}

        # Report
        result["report_md"] = generate_markdown_report(findings, entity_id=result["entity_id"], query=query, graph=(nodes, edges))
        from output_layer.evidence_report_generator.report import generate_html_report
        result["report_html"] = generate_html_report(findings, entity_id=result["entity_id"], query=query, graph=(nodes, edges))

        # Risk dashboard
        risk_scores = compute_risk_scores(findings)
        result["risk_scores"] = {"overall": risk_scores.overall, "by_risk_category": risk_scores.by_risk_category, "finding_count": risk_scores.finding_count}
        result["risk_dashboard_cli"] = format_dashboard_cli(risk_scores)

        result["audit_events"] = audit.get_events()
    except Exception as e:
        result["error"] = str(e)
        audit.record("pipeline_error", error=str(e))
        result["audit_events"] = audit.get_events()

    return result
