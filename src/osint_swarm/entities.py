from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Literal, Optional


EntityType = Literal["public_company", "private_company", "nonprofit", "individual", "unknown"]
SourceType = Literal[
    "sec_submissions",
    "sec_filing",
    "regulator_api",
    "regulator_report",
    "court_record",
    "news_article",
    "other",
]
RiskCategory = Literal["governance", "regulatory", "legal", "network", "other"]


@dataclass(frozen=True)
class Entity:
    """Canonical target for an investigation.

    Keep `identifiers` flexible (CIK/ticker/OpenCorporates/etc.) so we can support
    public companies, private entities, nonprofits, and individuals.
    """

    entity_id: str
    name: str
    entity_type: EntityType = "unknown"
    country: Optional[str] = None
    jurisdiction: Optional[str] = None
    identifiers: Dict[str, str] = field(default_factory=dict)
    aliases: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Evidence:
    """A single, citable claim about an entity with provenance.

    This is the core unit that later agents consume (not raw HTML/PDF).
    """

    evidence_id: str
    entity_id: str
    date: str  # ISO date (YYYY-MM-DD) if known
    source_type: SourceType
    risk_category: RiskCategory
    summary: str
    source_uri: str
    raw_location: Optional[str] = None  # path in data/raw for traceability
    confidence: float = 0.5  # 0..1
    attributes: Dict[str, Any] = field(default_factory=dict)  # extra structured fields

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

