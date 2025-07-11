from dataclasses import dataclass
from typing import Optional


@dataclass
class CreditCalculationResult:
    credits_used: float
    report_name: Optional[str] = None