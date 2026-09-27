from app.models.lead import Lead
from dataclasses import dataclass

@dataclass(frozen=True)
class LeadListResult:
    leads: list[Lead]
    page: int
    size: int
    total: int