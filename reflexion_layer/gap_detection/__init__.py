"""Gap detection: identify missing investigation coverage."""

from reflexion_layer.gap_detection.detector import detect_gaps
from reflexion_layer.gap_detection.types import Gap

__all__ = ["Gap", "detect_gaps"]
