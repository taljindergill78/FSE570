"""Cross-check: consistency checks across agent findings."""

from reflexion_layer.cross_check.checker import cross_check_findings
from reflexion_layer.cross_check.types import Conflict

__all__ = ["Conflict", "cross_check_findings"]
