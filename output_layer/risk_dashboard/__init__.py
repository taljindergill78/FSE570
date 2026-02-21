"""Risk dashboard: composite risk scores by dimension."""

from output_layer.risk_dashboard.dashboard import compute_risk_scores, format_dashboard_cli
from output_layer.risk_dashboard.types import RiskDashboardScores

__all__ = ["RiskDashboardScores", "compute_risk_scores", "format_dashboard_cli"]
